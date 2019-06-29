import datetime
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import PageView

@csrf_exempt
@login_required
def pageview(request):
    if request.method == 'POST':
        pageview = PageView(
            user=request.user,
            page=request.POST['page']
        )
        try:
            pageview.full_clean()
            pageview.save()
            return JsonResponse({'success': True})
        except ValidationError as e:
            return JsonResponse({'error': True})
    raise PermissionDenied

