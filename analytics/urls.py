from django.urls import path
from . import views

urlpatterns = [
    path("pageview/", views.pageview, name="pageview"),
]
