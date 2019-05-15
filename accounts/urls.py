from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.saml_login, name="login"),
    path("logout/", views.saml_logout, name="logout"),
    path("acs/", views.acs, name="acs"),
    path("metadata/", views.metadata, name="metadata"),
]
