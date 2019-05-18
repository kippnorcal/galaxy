from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from .models import Favorite, Report, Category

def navbar(request):
    categories = Category.objects.all().order_by('id')
    reports = Report.active.all()
    context = {"categories": categories, "reports": reports}
    return context

@csrf_exempt
def index(request):
    return render(request, "index.html")

@login_required(login_url='/login')
def profile(request):
    profile = request.user.profile
    favorites = Favorite.objects.filter(profile=profile)
    return render(request, "profile.html", {"profile": profile, "favorites": favorites})

@login_required(login_url='/login')
def report(request, report_id):
    report = Report.objects.get(pk=report_id)
    return render(request, "report.html", {"report": report})
