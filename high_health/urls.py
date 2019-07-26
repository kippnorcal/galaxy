from django.urls import path
from . import views

urlpatterns = [
    path("high_health/", views.high_health, name="high_health"),
    path("high_health/<str:school_level>", views.high_health, name="high_health"),
    path("high_health_overall/", views.high_health_agg, name="high_health_overall"),
    path(
        "high_health/chart_data/<int:metric_id>/<int:school_id>",
        views.chart_data,
        name="chart_data",
    ),
]
