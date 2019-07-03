from django.urls import path
from . import views

urlpatterns = [
    path("high_health/", views.high_health, name="high_health"),
    path("high_health/<str:school_level>", views.high_health, name="high_health"),
]
