from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from accounts.urls import router as account_router
from analytics.urls import router as analytics_router
from high_health.urls import router as high_health_router

router = routers.DefaultRouter()
router.registry.extend(account_router.registry)
router.registry.extend(analytics_router.registry)
router.registry.extend(high_health_router.registry)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("", include("catalog.urls")),
    path("", include("accounts.urls")),
    path("", include("high_health.urls")),
    path("", include("analytics.urls")),
]
