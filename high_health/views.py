from datetime import datetime
from dateutil.relativedelta import relativedelta
from itertools import chain, groupby
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg
from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import Site, SchoolLevel
from .models import EssentialQuestion, Metric, Measure


def last_updated(metric_id):
    return Measure.objects.filter(metric=metric_id).latest("date").date


def metrics(school_level):
    metrics = Metric.objects.filter(school_level=school_level)
    data = []
    for metric in metrics:
        metric_data = {
            "metric": metric,
            "last_updated": last_updated(metric.id),
            "measures": metric.measure_set.filter(
                school__school_level=school_level, is_current=True
            ).order_by("school"),
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
    start_date = f"{year-1}-07-01"
    end_date = f"{year}-06-30"
    return start_date, end_date


def month_order(month):
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
    return months[month]


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


@login_required
def chart_data(request, metric_id, school_id):
    cy_measures = year_bound_measures(metric_id, school_id)
    py_measures = year_bound_measures(metric_id, school_id, previous_year=True)
    cy_values = distinct_values(cy_measures)
    py_values = distinct_values(py_measures)
    months = distinct_months(py_measures, cy_measures)
    eoy_value = last_value(py_values)

    data = {
        "months": months,
        "py_label": chart_label(py_measures),
        "previous_year": py_values,
        "cy_label": chart_label(cy_measures),
        "current_year": cy_values,
        "goal": goal(eoy_value, metric_id),
    }
    return JsonResponse({"success": True, "data": data})


@login_required
def high_health(request, school_level=None):
    school_level = school_level or request.user.profile.site.school_level.id
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
        measures = (
            metric.measure_set.filter(is_current=True)
            .values("school__school_level")
            .annotate(avg_value=Avg("value"))
            .order_by("school__school_level")
        )
        metric_data = {
            "metric": metric,
            "last_updated": last_updated(metric.id),
            "measures": measures,
        }
        data.append(metric_data)

    context = {"school_levels": school_levels, "metrics": data}
    return render(request, "high_health_overall.html", context)
