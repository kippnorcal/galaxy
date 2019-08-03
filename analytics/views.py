import datetime
from django.shortcuts import render
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
from .models import PageView, Search, Login

from rest_framework import viewsets
from .serializers import PageViewSerializer, LoginSerializer, SearchSerializer


@csrf_exempt
@login_required
def pageview(request):
    if request.method == "POST":
        pageview = PageView(user=request.user, page=request.POST["page"])
        try:
            pageview.full_clean()
            pageview.save()
            return JsonResponse({"success": True})
        except ValidationError as e:
            return JsonResponse({"error": True})
    raise PermissionDenied


@csrf_exempt
@login_required
def click_through(request, search_id):
    if request.method == "POST":
        search = Search.objects.get(id=search_id)
        search.destination = request.POST["destination"]
        search.click_through_timestamp = timezone.now()
        try:
            search.full_clean()
            search.save()
            return JsonResponse({"success": True})
        except ValidationError as e:
            return JsonResponse({"error": True})
    raise PermissionDenied


class PageViewViewSet(viewsets.ModelViewSet):
    queryset = PageView.objects.all()
    serializer_class = PageViewSerializer
    http_method_names = ["get", "head", "options"]


class LoginViewSet(viewsets.ModelViewSet):
    queryset = Login.objects.all()
    serializer_class = LoginSerializer
    http_method_names = ["get", "head", "options"]


class SearchViewSet(viewsets.ModelViewSet):
    queryset = Search.objects.all()
    serializer_class = SearchSerializer
    http_method_names = ["get", "head", "options"]
