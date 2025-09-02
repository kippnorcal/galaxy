import logging
import math
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta
from itertools import chain, groupby
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import ObjectDoesNotExist
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

logger = logging.getLogger('console')


# Goal Colors
SUCCESS_COLOR = "#61B346"
SECONDARY_COLOR = "#84878A"
DANGER_COLOR = "#E8605D"


def last_updated(metric_id):
    try:
        return (
            Measure.objects.filter(metric=metric_id, is_current=True)
            .latest("date")
            .date
        )
    except Measure.DoesNotExist:
        return None


def metrics(school_level, schools):
    for school in schools:
        logger.debug(f"Calculating metrics for {school.name}")
    if school_level.name == "RS":
        order_by = "school__id"
    else:
        order_by = "school__name"
    metrics = (
        Metric.objects.filter(goal__school__school_level=school_level)
        .distinct()
        .order_by("id")
    )
    data = []
    for metric in metrics:
        if metric.is_active:
            measures = metric.measure_set.filter(school__school_level=school_level, is_current=True).order_by(order_by)
            if measures:
                measures = measures.filter(school__in=schools)
                metric_data = {
                    "metric": metric,
                    "last_updated": last_updated(metric.id),
                    "measures": measures,
                }
                data.append(metric_data)
    return sorted(data, key=lambda d: d["last_updated"], reverse=True)


def fill_missing_measures(measures, schools: List[Site]):
    missing_indexes = set([index for index, measure in enumerate(measures) if measure.school not in schools])
    filled_list = [measure if index not in missing_indexes else None for index, measure in enumerate(measures)]
    return filled_list


def last_value(values):
    if values:
        return values[-1]


def chart_label(measures):
    if measures:
        return measures.first().school_year


def school_year_range(today):
    if 7 <= today.month <= 12:
        year = today.year
    else:
        year = today.year - 1
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
    return [measure.school_year for measure in measures]


def year_bound_measures(metric_id, school_id, previous_year=False):
    latest_measure_date = (
        Measure.objects.filter(metric=metric_id, school=school_id).latest("date").date
    )
    if previous_year:
        a_year_ago = latest_measure_date - relativedelta(years=1)
        date_range = school_year_range(a_year_ago)
    else:
        date_range = school_year_range(latest_measure_date)
    return Measure.objects.filter(
        metric=metric_id, school=school_id, date__range=date_range
    ).order_by("date")


def distinct_values(measures):
    return [measure.value for measure in measures]


def find_axis_max(values, goal):
    max_value = max(values)
    if math.ceil(goal + 2) > math.ceil(max_value):
        axis_max = math.ceil(goal + 2)
    else:
        axis_max = math.ceil(max_value + 2)
    return axis_max


def find_axis_min(values, goal):
    min_value = min(values)
    if math.floor(goal - 2) <= math.floor(min_value - 2):
        axis_min = math.floor(goal - 2)
    else:
        axis_min = math.floor(min_value - 2)
    return axis_min


def yoy_color_eval(goal, value):
    if goal.goal_type.upper() == "ABOVE":
        if value >= goal.target:
            return SUCCESS_COLOR
        elif goal.previous_outcome <= value < goal.target:
            return SECONDARY_COLOR
        else:
            return DANGER_COLOR
    else:
        if value <= goal.target:
            return SUCCESS_COLOR
        elif goal.previous_outcome >= value > goal.target:
            return SECONDARY_COLOR
        else:
            return DANGER_COLOR


def mom_color_eval(goal, value, previous, bypass=False):
    if bypass:
        return SECONDARY_COLOR

    if goal.goal_type.upper() == "ABOVE":
        if value < previous:
            return DANGER_COLOR
        elif value >= goal.target and value >= previous:
            return SUCCESS_COLOR
        else:
            return SECONDARY_COLOR
    else:
        if value > previous:
           return DANGER_COLOR
        elif value <= goal.target and value <= previous:
            logger.info(previous)
            return SUCCESS_COLOR
        else:
            return SECONDARY_COLOR


def get_last_years_value(month, measures):
    """This function is grabbing the data from this time last year for MoM comparison"""
    try:
        return [measure for measure in measures if measure.month == month][0].value
    except IndexError:
        return None


def monthly_data(metric_id, school_id):
    cy_measures = year_bound_measures(metric_id, school_id)
    py_measures = year_bound_measures(metric_id, school_id, previous_year=True)
    cy_values = distinct_values(cy_measures)
    py_values = distinct_values(py_measures)
    months = distinct_months(py_measures, cy_measures)
    values = cy_values + py_values
    non_null_values = list(filter(None, values))
    goal = Goal.objects.get(metric=metric_id, school=school_id)
    target = round(goal.target, 2)
    goal_type = goal.goal_type
    axis_min = find_axis_min(non_null_values, target)
    axis_max = find_axis_max(non_null_values, target)

    #  The below block is part of a patch to change how MoM measures are evaluated
    current_month = cy_measures.reverse()[0].month
    last_year_value = get_last_years_value(current_month, py_measures)

    goal_color = mom_color_eval(goal, cy_values[-1], last_year_value)

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
    non_null_values = list(filter(None, values))
    goal = Goal.objects.get(metric=metric_id, school=school_id)
    target = round(goal.target)
    goal_type = goal.goal_type
    axis_min = find_axis_min(non_null_values, target)
    axis_max = find_axis_max(non_null_values, target)
    goal_color = yoy_color_eval(goal, values[-1])

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


def check_permissions(user):
    allowed_groups = ["High Health", "Site Admin"]
    return (
        user.groups.filter(name__in=allowed_groups).exists()
        or user.profile.job_title.role.permission_groups.filter(
            name__in=allowed_groups
        ).exists()
    )


def unauthorized(request):
    return render(request, "403.html")


@login_required
@user_passes_test(
    check_permissions, login_url="/unauthorized", redirect_field_name=None
)
def chart_data(request, metric_id, school_id):
    frequency = Metric.objects.get(pk=metric_id).frequency
    if frequency == "MoM":
        data = monthly_data(metric_id, school_id)
    elif frequency == "YoY":
        data = yearly_data(metric_id, school_id)

    return JsonResponse({"success": True, "data": data})


@login_required
@user_passes_test(
    check_permissions, login_url="/unauthorized", redirect_field_name=None
)
def high_health(request, school_level=None):
    school_level = SchoolLevel.objects.get(pk=school_level)
    if school_level.name == "RS":
        schools = Site.objects.filter(school_level=school_level).exclude(is_active=False).order_by("id")
    else:
        schools = Site.objects.filter(school_level=school_level).exclude(is_active=False).order_by("name")
    context = {
        "school_level": school_level,
        "schools": schools,
        "metrics": metrics(school_level, schools),
    }
    return render(request, "high_health.html", context)


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
