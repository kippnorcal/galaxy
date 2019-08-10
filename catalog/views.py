from os import getenv
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
from django.db.models import Max, Count

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from .models import Favorite, Feedback, Report, Category, PublicStat, SubCategory
from analytics.models import Search, PageView
import requests


def navbar(request):
    categories = Category.objects.filter(report__isnull=False).distinct()
    reports = Report.active.for_user(request.user)
    context = {"categories": categories, "reports": reports}
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


@login_required(login_url="/login")
def profile(request):
    profile = request.user.profile
    favorites = Favorite.objects.filter(profile=profile)
    recently_viewed = (
        PageView.objects.filter(user=request.user)
        .values("page")
        .annotate(views=Count("page"), timestamp=Max("timestamp"))
        .order_by("-timestamp")
    )
    context = {
        "profile": profile,
        "favorites": favorites,
        "recently_viewed": recently_viewed,
    }
    return render(request, "profile.html", context)


@login_required(login_url="/login")
def report(request, report_id):
    report = get_object_or_404(Report, pk=report_id, is_embedded=True)
    is_favorite = Favorite.objects.filter(
        report=report_id, profile=request.user.profile
    ).exists()
    favorited_by = Favorite.objects.filter(report=report_id).count()
    auth_ticket = get_iframe_auth_ticket(request.user, report.site_root)
    context = {
        "report": report,
        "is_favorite": is_favorite,
        "favorited_by": favorited_by,
        "auth_ticket": auth_ticket,
    }
    feedback = (
        Feedback.objects.filter(user=request.user).filter(report=report_id).last()
    )
    avg_feedback = Feedback.objects.filter(report=report_id).aggregate(Avg("score"))
    if feedback:
        context["feedback"] = feedback
    if avg_feedback and avg_feedback["score__avg"] is not None:
        context["avg_feedback"] = round(avg_feedback["score__avg"], 1)
    page_views = PageView.objects.filter(page=request.build_absolute_uri())
    if page_views:
        context["viewed_by"] = len(page_views)
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
        reports = Report.objects.annotate(
            search=SearchVector("name", "category", "description")
        ).filter(search=search_term)
        context = {
            "reports": reports,
            "search_term": search_term,
            "search_id": tracking.id,
        }
        return render(request, "search.html", context)
