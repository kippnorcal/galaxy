from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("attrs/", views.attrs, name="attrs"),
    path("metadata/", views.metadata, name="metadata"),
]
