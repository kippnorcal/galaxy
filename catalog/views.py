from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils


@csrf_exempt
def index(request):
    attributes = None
    # print(request.session.items())
    if "samlUserdata" in request.session:
        print(True)
        paint_logout = True
        if len(request.session["samlUserdata"]) > 0:
            attrs = request.session["samlUserdata"].items()
            attrs = dict(attrs)
            attributes = {
                'profile_pic': attrs['Profile Pic'][0],
                'email': attrs['User.email'][0],
                'name': f"{attrs['User.FirstName'][0]} {attrs['User.LastName'][0]}",
                'job': attrs['Job Title'][0],
            }

    return render(request, "index.html", {"attributes": attributes})

@login_required(login_url='/login')
def profile(request):
    paint_logout = False
    attributes = False

    if "samlUserdata" in request.session:
        paint_logout = True
        if len(request.session["samlUserdata"]) > 0:
            attrs = request.session["samlUserdata"].items()
            attrs = dict(attrs)
            attributes = {
                'profile_pic': attrs['Profile Pic'][0],
                'email': attrs['User.email'][0],
                'name': f"{attrs['User.FirstName'][0]} {attrs['User.LastName'][0]}",
                'job': attrs['Job Title'][0],
            }
    return render(
        request, "profile.html", {"paint_logout": paint_logout, "attributes": attributes}
    )
