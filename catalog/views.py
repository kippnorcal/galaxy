from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from .models import Favorite, Report


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
    report = get_object_or_404(Report, pk=report_id, is_embedded=True)
    return render(request, "report.html", {"report": report})
