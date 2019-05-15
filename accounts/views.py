from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils


def prepare_django_request(request):
    result = {
        "https": "on" if request.is_secure() else "off",
        "http_host": request.META["HTTP_HOST"],
        "script_name": request.META["PATH_INFO"],
        "server_port": request.META["SERVER_PORT"],
        "get_data": request.GET.copy(),
        "post_data": request.POST.copy(),
    }
    return result


def init_saml_auth(request):
    req = prepare_django_request(request)
    auth = OneLogin_Saml2_Auth(req, custom_base_path=settings.SAML_FOLDER)
    return auth

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

def login(request):
    auth = init_saml_auth(request)
    return HttpResponseRedirect(auth.login())

def logout(request):
    auth = init_saml_auth(request)
    name_id = request.session["samlNameId"]
    session_index = request.session["samlSessionIndex"]
    return HttpResponseRedirect(
        auth.logout(name_id=name_id, session_index=session_index)
    )

@csrf_exempt
def acs(request):
    req = prepare_django_request(request)
    auth = init_saml_auth(request)
    auth.process_response()
    errors = auth.get_errors()
    not_auth_warn = not auth.is_authenticated()
    print(OneLogin_Saml2_Utils.get_self_url(req))

    print(req["post_data"]["RelayState"])
    if not errors:
        request.session["samlUserdata"] = auth.get_attributes()
        request.session["samlNameId"] = auth.get_nameid()
        request.session["samlSessionIndex"] = auth.get_session_index()
        base_url = OneLogin_Saml2_Utils.get_self_url(req)
        return HttpResponseRedirect(
            auth.redirect_to(f"{base_url}/attrs")
        )
    else:
        if auth.get_settings().is_debug_active():
            error_reason = auth.get_last_error_reason()


