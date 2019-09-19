from datetime import datetime
from dateutil.relativedelta import relativedelta
from itertools import chain, groupby
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from accounts.models import Site, SchoolLevel
from .models import EssentialQuestion, Metric, Measure, Goal

from rest_framework import viewsets, filters
from .serializers import (
    EssentialQuestionSerializer,
    MetricSerializer,
    GoalSerializer,
    MeasureSerializer,
)


def last_updated(metric_id):
    try:
        return Measure.objects.filter(metric=metric_id).latest("date").date
    except Measure.DoesNotExist:
        return None


def metrics(school_level):
    metrics = (
        Metric.objects.filter(goal__school__school_level=school_level)
        .distinct()
        .order_by("id")
    )
    data = []
    for metric in metrics:
        measures = metric.measure_set.filter(
            school__school_level=school_level, is_current=True
        ).order_by("school")
        if measures:
            metric_data = {
                "metric": metric,
                "last_updated": last_updated(metric.id),
                "measures": measures,
            }
            data.append(metric_data)
    return data


def last_value(values):
    if values:
        return values[-1]


def chart_label(measures):
    if measures:
        return measures.first().school_year


def school_year_range(today=datetime.today()):
    year = int(today.strftime("%Y"))
    start_date = f"{year}-07-01"
    end_date = f"{year+1}-06-30"
    return start_date, end_date


def month_order(month=None):
    months = {
        "Jul": 0,
        "Aug": 1,
        "Sep": 2,
        "Oct": 3,
        "Nov": 4,
        "Dec": 5,
        "Jan": 6,
        "Feb": 7,
        "Mar": 8,
        "Apr": 9,
        "May": 10,
        "Jun": 11,
    }
    if month:
        return months[month]
    else:
        return list(months.keys())


def goal(eoy_value, metric_id):
    metric = Metric.objects.get(pk=metric_id)
    performance_goal = round(metric.performance_goal)
    if eoy_value is None:
        return performance_goal
    growth_goal = round(eoy_value + metric.growth_goal)
    if growth_goal <= performance_goal:
        return growth_goal
    else:
        return performance_goal


def distinct_months(prior_year_measures, current_year_measures):
    py_months = [measure.month_name for measure in prior_year_measures]
    cy_months = [measure.month_name for measure in current_year_measures]
    months = list(set(py_months + cy_months))
    months.sort(key=month_order)
    return months


def distinct_years(measures):
    return [measure.year for measure in measures]


def year_bound_measures(metric_id, school_id, previous_year=False):
    if previous_year:
        a_year_ago = datetime.today() - relativedelta(years=1)
        date_range = school_year_range(a_year_ago)
    else:
        date_range = school_year_range()
    return Measure.objects.filter(
        metric=metric_id, school=school_id, date__range=date_range
    ).order_by("date")


def distinct_values(measures):
    return [measure.value for measure in measures]


def find_axis_max(values, goal):
    max_value = max(values)
    if goal + 3 >= 100 or max_value + 1 >= 100:
        axis_max = 100
    elif goal + 3 > max_value:
        axis_max = round(goal + 3)
    else:
        axis_max = round(max_value + 1)
    return axis_max


def find_axis_min(values, goal):
    min_value = min(values)
    if goal - 1 <= min_value - 3:
        axis_min = round(goal - 1)
    else:
        axis_min = round(min_value - 3)
    return axis_min


def get_goal_color(goal, value):
    if goal.goal_type == "ABOVE":
        if value >= goal.target:
            return "#6CC04A"  # kipp green
        elif value < goal.target:
            return "#dc3545"  # crimson
    elif goal.goal_type == "BELOW":
        if value <= goal.target:
            return "#6CC04A"  # kipp green
        elif value > goal.target:
            return "#dc3545"  # crimson


def monthly_data(metric_id, school_id):
    cy_measures = year_bound_measures(metric_id, school_id)
    py_measures = year_bound_measures(metric_id, school_id, previous_year=True)
    cy_values = distinct_values(cy_measures)
    py_values = distinct_values(py_measures)
    months = distinct_months(py_measures, cy_measures)
    values = cy_values + py_values
    goal = Goal.objects.get(metric=metric_id, school=school_id)
    target = round(goal.target)
    goal_type = goal.goal_type
    axis_min = find_axis_min(values, target)
    axis_max = find_axis_max(values, target)
    goal_color = get_goal_color(goal, cy_values[-1])

    return {
        "frequency": "monthly",
        "months": months,
        "py_label": chart_label(py_measures),
        "previous_year": py_values,
        "cy_label": chart_label(cy_measures),
        "current_year": cy_values,
        "goal": target,
        "goal_type": goal_type,
        "goal_color": goal_color,
        "metric": Metric.objects.get(pk=metric_id).name,
        "axis_min": axis_min,
        "axis_max": axis_max,
    }


def yearly_data(metric_id, school_id):
    metric = Metric.objects.get(pk=metric_id).name
    measures = Measure.objects.filter(metric=metric_id, school=school_id).order_by(
        "date"
    )
    values = distinct_values(measures)
    goal = Goal.objects.get(metric=metric_id, school=school_id)
    target = round(goal.target)
    goal_type = goal.goal_type
    axis_min = find_axis_min(values, target)
    axis_max = find_axis_max(values, target)
    goal_color = get_goal_color(goal, values[-1])

    return {
        "frequency": "yearly",
        "years": distinct_years(measures),
        "label": None,
        "values": values,
        "goal": target,
        "goal_type": goal_type,
        "goal_color": goal_color,
        "metric": metric,
        "axis_min": axis_min,
        "axis_max": axis_max,
    }


@login_required
def chart_data(request, metric_id, school_id):
    frequency = Metric.objects.get(pk=metric_id).frequency
    if frequency == "MoM":
        data = monthly_data(metric_id, school_id)
    elif frequency == "YoY":
        data = yearly_data(metric_id, school_id)

    return JsonResponse({"success": True, "data": data})


@login_required
def chart_data_agg(request, metric_id, school_level_id):
    metric = Metric.objects.get(pk=metric_id)
    cy_measures = metric.measure_set.filter(
        school__school_level=school_level_id, date__range=school_year_range()
    )
    cy_label = chart_label(cy_measures)
    cy_agg = (
        cy_measures.values("date").annotate(avg_value=Avg("value")).order_by("date")
    )
    cy_values = [value["avg_value"] for value in cy_agg]
    a_year_ago = datetime.today() - relativedelta(years=1)
    py_measures = metric.measure_set.filter(
        school__school_level=school_level_id, date__range=school_year_range(a_year_ago)
    )
    py_label = chart_label(py_measures)
    py_agg = (
        py_measures.values("date").annotate(avg_value=Avg("value")).order_by("date")
    )
    py_values = [value["avg_value"] for value in py_agg]
    data = {
        "months": month_order()[1:],
        "py_label": py_label,
        "previous_year": py_values,
        "cy_label": cy_label,
        "current_year": cy_values,
        "goal": round(
            Goal.objects.filter(
                metric=metric_id, school__school_level=school_level_id
            ).aggregate(avg_goal=Avg("target"))["avg_goal"],
            2,
        ),
        "metric": Metric.objects.get(pk=metric_id).name,
    }
    return JsonResponse({"success": True, "data": data})


def get_school_level(user):
    if user.profile.site.name == "RSO":
        return 1
    else:
        return user.profile.site.school_level.id


@login_required
def high_health(request, school_level=None):
    # TODO: Convert to query school level by name instead of id
    school_level = school_level or get_school_level(request.user)
    context = {
        "school_level": SchoolLevel.objects.get(pk=school_level),
        "schools": Site.objects.filter(school_level=school_level),
        "metrics": metrics(school_level),
        "school_levels": SchoolLevel.objects.all(),
    }
    return render(request, "high_health.html", context)


@login_required
def high_health_agg(request):
    school_levels = SchoolLevel.objects.all()
    metrics = Metric.objects.all()
    data = []
    for metric in metrics:
        measures_data = []
        measures = (
            metric.measure_set.filter(is_current=True)
            .values("school__school_level")
            .annotate(avg_value=Avg("value"))
            .order_by("school__school_level")
        )
        for measure in measures:
            measure_data = {
                "school_level": school_levels.get(pk=measure["school__school_level"]),
                "value": measure["avg_value"],
                "goal": Goal.objects.values("goal_type")
                .annotate(avg_goal=Avg("target"))
                .filter(
                    metric=metric, school__school_level=measure["school__school_level"]
                )
                .order_by("goal_type")
                .first(),
            }
            measures_data.append(measure_data)
        metric_data = {
            "metric": metric,
            "last_updated": last_updated(metric.id),
            "measures": measures_data,
        }
        data.append(metric_data)
    context = {"school_levels": school_levels, "metrics": data}
    return render(request, "high_health_overall.html", context)


class EssentialQuestionViewSet(viewsets.ModelViewSet):
    queryset = EssentialQuestion.objects.all()
    serializer_class = EssentialQuestionSerializer


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer


class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.all()
    serializer_class = MeasureSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("is_current",)

