from .models import EssentialQuestion, Goal, Metric, Measure
from accounts.models import Site
from catalog.models import Report
from django.contrib.auth.models import User
from rest_framework import serializers


class EssentialQuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EssentialQuestion
        fields = ("id", "name", "description")


class MetricSerializer(serializers.HyperlinkedModelSerializer):
    essential_question = serializers.PrimaryKeyRelatedField(
        queryset=EssentialQuestion.objects.all()
    )
    report = serializers.PrimaryKeyRelatedField(queryset=Report.objects.all())

    class Meta:
        model = Metric
        fields = (
            "id",
            "name",
            "definition",
            "essential_question",
            "frequency",
            "report",
            "date",
        )


class GoalSerializer(serializers.HyperlinkedModelSerializer):
    metric = serializers.PrimaryKeyRelatedField(queryset=Metric.objects.all())
    school = serializers.PrimaryKeyRelatedField(
        queryset=Site.objects.filter(is_school=True)
    )

    class Meta:
        model = Goal
        fields = ("id", "metric", "school", "goal_type", "previous_outcome", "target")


class MeasureSerializer(serializers.HyperlinkedModelSerializer):
    metric = serializers.PrimaryKeyRelatedField(queryset=Metric.objects.all())
    school = serializers.PrimaryKeyRelatedField(
        queryset=Site.objects.filter(is_school=True)
    )

    class Meta:
        model = Measure
        fields = ("id", "metric", "school", "value", "date", "is_current")
