from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"roles", views.RoleViewSet)
router.register(r"jobs", views.JobViewSet)
router.register(r"school_levels", views.SchoolLevelViewSet)
router.register(r"sites", views.SiteLevelViewSet)
router.register(r"profiles", views.ProfileViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("login/", views.saml_login, name="login"),
    path("logout/", views.saml_logout, name="logout"),
    path("acs/", views.acs, name="acs"),
    path("metadata/", views.metadata, name="metadata"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
