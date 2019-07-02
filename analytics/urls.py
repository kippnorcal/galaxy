from django.urls import path
from . import views

urlpatterns = [
    path("pageview/", views.pageview, name="pageview"),
    path("click_through/<int:search_id>", views.click_through, name="click_through"),
]
