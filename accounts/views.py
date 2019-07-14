from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login, logout

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from .models import Profile
from analytics.models import Login


def prepare_django_request(request):
    result = {
        "https": "on" if request.is_secure() else "off",
        "http_host": request.META["HTTP_HOST"],
        "script_name": request.META["PATH_INFO"],
        "get_data": request.GET.copy(),
        "post_data": request.POST.copy(),
    }
    return result


def init_saml_auth(request):
    req = prepare_django_request(request)
    auth = OneLogin_Saml2_Auth(req, custom_base_path=settings.SAML_FOLDER)
    return auth


def get_saml_attributes(request):
    if "samlUserdata" in request.session:
        paint_logout = True
        if len(request.session["samlUserdata"]) > 0:
            attrs = request.session["samlUserdata"].items()
            attrs = dict(attrs)
            attributes = {
                "profile_pic": attrs["Profile Pic"][0],
                "email": attrs["User.email"][0],
                "first_name": attrs["User.FirstName"][0],
                "last_name": attrs["User.LastName"][0],
                "job": attrs["Job Title"][0],
                "username": attrs["PersonImmutableID"][0],
            }
        return attributes


def find_or_create_user(request):
    attrs = get_saml_attributes(request)
    if User.objects.filter(email=attrs["email"]).exists():
        user = User.objects.get(email=attrs["email"])
    else:
        user = User(
            username=attrs["username"],
            first_name=attrs["first_name"],
            last_name=attrs["last_name"],
            email=attrs["email"],
        )
        user.save()
    return user


def connect_profile(user):
    if Profile.objects.filter(email__iexact=user.email).exists():
        profile = Profile.objects.get(email__iexact=user.email)
        profile.user = user
        profile.save()


def save_avatar(request, user):
    attrs = get_saml_attributes(request)
    try:
        url = attrs["profile_pic"]
        user.profile.avatar_url = url
        user.profile.save()
    except:
        pass


def metadata(request):
    saml_settings = OneLogin_Saml2_Settings(
        settings=None, custom_base_path=settings.SAML_FOLDER, sp_validation_only=True
    )
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)

    if len(errors) == 0:
        resp = HttpResponse(content=metadata, content_type="text/xml")
    else:
        resp = HttpResponseServerError(content=", ".join(errors))
    return resp


def saml_login(request):
    auth = init_saml_auth(request)
    return HttpResponseRedirect(auth.login())


def saml_logout(request):
    auth = init_saml_auth(request)
    name_id = None
    session_index = None
    if "samlNameId" in request.session:
        name_id = request.session["samlNameId"]
    if "samlSessionIndex" in request.session:
        session_index = request.session["samlSessionIndex"]

    logout(request)
    return HttpResponseRedirect(
        auth.logout(name_id=name_id, session_index=session_index)
    )


def track_login(request, user):
    tracking = Login(
        user=user,
        referrer=request.META.get("HTTP_REFERER"),
        user_agent=request.META.get("HTTP_USER_AGENT"),
        ip_address=request.META.get("REMOTE_ADDR"),
    )
    tracking.full_clean()
    tracking.save()


@csrf_exempt
def acs(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(request)
    auth.process_response()
    errors = auth.get_errors()
    not_auth_warn = not auth.is_authenticated()

    if not errors:
        request.session["samlUserdata"] = auth.get_attributes()
        request.session["samlNameId"] = auth.get_nameid()
        request.session["samlSessionIndex"] = auth.get_session_index()
        base_url = OneLogin_Saml2_Utils.get_self_url(req)
        user = find_or_create_user(request)
        login(request, user)
        track_login(request, user)
        connect_profile(user)
        save_avatar(request, user)
        return HttpResponseRedirect(auth.redirect_to(f"{base_url}/profile"))
    else:
        if auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()

