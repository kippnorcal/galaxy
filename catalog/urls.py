from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"categories", views.CategoryViewSet)
router.register(r"subcategories", views.SubCategoryViewSet)
router.register(r"reports", views.ReportViewSet)
router.register(r"favorites", views.FavoriteViewSet)
router.register(r"feedback", views.FeedbackViewSet)


urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("report/<int:report_id>", views.report, name="report"),
    path("feedback/<int:report_id>/", views.feedback_form, name="feedback_form"),
    path("favorite/<int:report_id>/", views.favorite_form, name="favorite_form"),
    path("search", views.search, name="search"),
]
