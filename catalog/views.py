from django.conf import settings
from django.core.exceptions import PermissionDenied, ValidationError
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils

from .models import Favorite, Feedback, Report


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
    context = { "report": report }
    feedback = Feedback.objects.filter(user=request.user).filter(report=report_id).last()
    if feedback:
        context["feedback"] = feedback

    return render(request, "report.html", context)

@login_required
def feedback_form(request, report_id):
    print(request.method)
    if request.method == 'POST':
        feedback = Feedback(
            user=request.user,
            report=Report.objects.get(pk=report_id),
            score=request.POST['score'],
            comment=request.POST['comment']
        )
        try:
            feedback.full_clean()
            feedback.save()
            return JsonResponse({'success': True, 'score':request.POST['score']})
        except ValidationError as e:
            message = dict(e)
            if message.get('score'):
                errors = str(message.get('score')[0])
                return JsonResponse({'error': errors})
    raise PermissionDenied
