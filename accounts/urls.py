from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("acs/", views.acs, name="acs"),
    path("metadata/", views.metadata, name="metadata"),
]
