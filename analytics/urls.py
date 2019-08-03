from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r"page_views", views.PageViewViewSet)
router.register(r"logins", views.LoginViewSet)
router.register(r"searches", views.SearchViewSet)


urlpatterns = [
    path("pageview/", views.pageview, name="pageview"),
    path("click_through/<int:search_id>", views.click_through, name="click_through"),
]
