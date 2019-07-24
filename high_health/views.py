from datetime import datetime
from dateutil.relativedelta import relativedelta
from itertools import chain, groupby
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import Site
from .models import EssentialQuestion, Metric, Measure


def metrics(measures):
    metrics_data = []
    metrics = set([measure.metric for measure in measures])
    schools = set([measure.school for measure in measures])
    for metric in metrics:
        metric_data = {}
        metric_data["metric"] = metric
        measures_data = []
        dates = []
        for school in schools:
            measure_data = {}
            measure_data["school"] = school
            measure_data["measure"] = None
            for measure in measures:
                if measure.metric == metric and measure.school == school:
                    measure_data["measure"] = measure
                    dates.append(measure.date)
            measures_data.append(measure_data)
        metric_data["last_updated"] = max(dates)
        metric_data["measures"] = measures_data
        metrics_data.append(metric_data)
    return metrics_data


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


def target(eoy_value, metric_id):
    metric = Metric.objects.get(pk=metric_id)
    performance_goal = round(metric.performance_goal)
    if eoy_value is None:
        return performance_goal
    growth_goal = round(eoy_value + metric.growth_goal)
    if growth_goal <= performance_goal:
        return growth_goal
    else:
        return performance_goal


def get_distinct_months(prior_year_measures, current_year_measures):
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


@login_required
def chart_data(request, metric_id, school_id):
    cy_measures = year_bound_measures(metric_id, school_id)
    py_measures = year_bound_measures(metric_id, school_id, previous_year=True)
    cy_values = [measure.value for measure in cy_measures]
    py_values = [measure.value for measure in py_measures]
    months = get_distinct_months(py_measures, cy_measures)
    eoy_value = last_value(py_values)
    goal = target(eoy_value, metric_id)

    data = {
        "months": months,
        "py_label": chart_label(py_measures),
        "previous_year": py_values,
        "cy_label": chart_label(cy_measures),
        "current_year": cy_values,
        "goal": goal,
    }
    return JsonResponse({"success": True, "data": data})


@login_required
def high_health(request, school_level=None):
    if school_level is None:
        school_level = request.user.profile.site.school_level
    measures = Measure.objects.filter(
        school__school_level=school_level, is_current=True
    ).order_by("metric__essential_question", "metric", "school")
    schools = set([measure.school for measure in measures])
    school_levels = [
        {"name": "Elementary Schools", "url": "/high_health/1"},
        {"name": "Middle Schools", "url": "/high_health/2"},
        {"name": "High Schools", "url": "/high_health/4"},
        {"name": "K-8 Schools", "url": "/high_health/3"},
    ]
    context = {
        "schools": schools,
        "metrics": metrics(measures),
        "school_levels": school_levels,
    }
    return render(request, "high_health.html", context)

