from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"essential_questions", views.EssentialQuestionViewSet)
router.register(r"metrics", views.MetricViewSet)
router.register(r"goals", views.GoalViewSet)
router.register(r"measures", views.MeasureViewSet)


urlpatterns = [
    path("high_health/", views.high_health, name="high_health"),
    path("high_health/<str:school_level>", views.high_health, name="high_health"),
    path("unauthorized/", views.unauthorized, name="unauthorized"),
    path(
        "high_health/chart_data/<int:metric_id>/<int:school_id>",
        views.chart_data,
        name="chart_data",
    ),
]
