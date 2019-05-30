from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("report/<int:report_id>", views.report, name="report"),
    path('feedback/<int:report_id>/', views.feedback_form, name='feedback_form'),
    path('favorite/<int:report_id>/', views.favorite_form, name='favorite_form'),
    path("search", views.search, name="search"),
]
