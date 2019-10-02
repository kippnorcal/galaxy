from os import getenv
import re
from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.urls import reverse
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseServerError,
    JsonResponse,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.contrib.postgres.search import SearchVector
from django.db.models import Max, Count, Q

from .models import Favorite, Feedback, Report, Category, PublicStat, SubCategory
from accounts.models import SchoolLevel, Profile
from analytics.models import Search, PageView
import requests
from rest_framework import viewsets
from .serializers import (
    CategorySerializer,
    SubCategorySerializer,
    ReportSerializer,
    FavoriteSerializer,
    FeedbackSerializer,
)
import rollbar


def navbar(request):
    if request.user.is_anonymous:
        categories = None
        reports = None
        subcategories = None
        school_levels = None
    if request.user.is_authenticated:
        reports = Report.active.for_user(request.user)
        if reports:
            category_list = reports.values_list("category").distinct()
            categories = Category.objects.filter(id__in=category_list).order_by("id")
            subcategory_list = reports.values_list("subcategory").distinct()
            subcategories = SubCategory.objects.filter(
                id__in=subcategory_list
            ).order_by("id")
            school_levels = SchoolLevel.objects.all().order_by("id")
        else:
            categories = None
            reports = None
            subcategories = None
            school_levels = None
    context = {
        "categories": categories,
        "reports": reports,
        "subcategories": subcategories,
        "school_levels": school_levels,
    }
    return context


def get_iframe_auth_ticket(user, site):
    url = getenv("TABLEAU_TRUSTED_URL")
    domain = getenv("USER_DOMAIN")
    r = requests.post(url, data={"username": f"{domain}\{user}", "target_site": site})
    return r.text


@csrf_exempt
def index(request):
    stats = PublicStat.objects.all().order_by("id")
    return render(request, "index.html", context={"stats": stats})


@login_required
def missing_profile(request):
    profile = None
    rollbar.report_message(f"{request.user} does not have a profile set up.")
    return render(request, "missing_profile.html", profile)


@login_required(login_url="/login")
def profile(request):
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect("/missing_profile/")
    favorites = Favorite.objects.filter(profile=profile)
    recently_viewed = (
        PageView.objects.filter(user=request.user)
        .filter(Q(page__contains="report") | Q(page__contains="high_health"))
        .values("page")
        .annotate(views=Count("page"), timestamp=Max("timestamp"))
        .order_by("-timestamp")
    )
    pages = []
    for page in recently_viewed:
        try:
            page_id = re.findall("\\d+", page["page"])
            page_id = page_id[0] if page_id else None
            if "report" in page["page"]:
                page["display_name"] = Report.objects.get(pk=page_id)
            elif "high_health" in page["page"]:
                if page_id is not None:
                    school_level = SchoolLevel.objects.get(pk=page_id)
                    page["display_name"] = f"High Health ({school_level.display_name})"
            else:
                page["display_name"] = "High Health"
            pages.append(page)
        except Report.DoesNotExist:
            pass
        except ValueError:
            pass

    context = {"profile": profile, "favorites": favorites, "recently_viewed": pages}
    return render(request, "profile.html", context)


@login_required(login_url="/login")
def report(request, report_id):
    report_query = Report.active.for_user(request.user)
    report = get_object_or_404(report_query, pk=report_id, is_embedded=True)
    is_favorite = Favorite.objects.filter(
        report=report_id, profile=request.user.profile
    ).exists()
    favorited_by = Favorite.objects.filter(report=report_id).count()
    auth_ticket = get_iframe_auth_ticket(request.user, report.target_site())
    context = {
        "report": report,
        "is_favorite": is_favorite,
        "favorited_by": favorited_by,
        "auth_ticket": auth_ticket,
        "viewed_by": 0,
        "ssl": getenv("SSL", default=0),
    }
    feedback = (
        Feedback.objects.filter(user=request.user).filter(report=report_id).last()
    )
    avg_feedback = Feedback.objects.filter(report=report_id).aggregate(Avg("score"))
    if feedback:
        context["feedback"] = feedback
    if avg_feedback and avg_feedback["score__avg"] is not None:
        context["avg_feedback"] = round(avg_feedback["score__avg"], 1)
    if getenv("SSL", default=0):
        page = request.build_absolute_uri()
        page = page.replace("http", "https")
    else:
        page = request.build_absolute_uri()
    page_views = PageView.objects.filter(page=page)
    page_views = page_views.aggregate(views=Count("user", distinct=True))
    if page_views:
        context["viewed_by"] = page_views["views"]
    return render(request, "report.html", context)


@login_required
def feedback_form(request, report_id):
    if request.method == "POST":
        feedback = Feedback(
            user=request.user,
            report=Report.objects.get(pk=report_id),
            score=request.POST["score"],
            comment=request.POST["comment"],
        )
        try:
            feedback.full_clean()
            feedback.save()
            avg_feedback = Feedback.objects.filter(report=report_id).aggregate(
                Avg("score")
            )
            avg_feedback = round(avg_feedback["score__avg"], 1)
            return JsonResponse(
                {
                    "success": True,
                    "score": request.POST["score"],
                    "avg_feedback": avg_feedback,
                }
            )
        except ValidationError as e:
            message = dict(e)
            if message.get("score"):
                errors = str(message.get("score")[0])
                return JsonResponse({"error": errors})
    raise PermissionDenied


@login_required
def favorite_form(request, report_id):
    if request.method == "POST":
        favorite = Favorite.objects.filter(
            profile=request.user.profile, report=report_id
        ).exists()
        if favorite:
            Favorite.objects.filter(
                profile=request.user.profile, report=report_id
            ).delete()
        else:
            Favorite.objects.create(profile=request.user.profile, report_id=report_id)
        favorited_by = Favorite.objects.filter(report=report_id).count()
        return JsonResponse({"success": True, "favorited_by": favorited_by})
    raise PermissionDenied


@login_required
def search(request):
    if request.method == "POST":
        search_term = request.POST["search-term"]
        tracking = Search(user=request.user, search_term=search_term)
        tracking.save()
        reports = (
            Report.active.for_user(request.user)
            .annotate(search=SearchVector("name", "category", "description"))
            .filter(search=search_term)
        )
        context = {
            "search_results": reports,
            "search_term": search_term,
            "search_id": tracking.id,
        }
        return render(request, "search.html", context)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
