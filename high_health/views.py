from datetime import datetime
from dateutil.relativedelta import relativedelta
from itertools import chain, groupby
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Site
from .models import EssentialQuestion, Metric, Measure
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse


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


def eoy_value(measures, school):
    for measure in measures:
        # TODO: Set this to max date from previous year
        if measure.school == school and measure.date.month == 6:
            return measure


def metric_target(metric, measures, school):
    eoy_results = eoy_value(measures, school)
    performance_goal = metric.performance_goal
    growth_goal = eoy_results.value + metric.growth_goal
    if growth_goal <= performance_goal:
        return growth_goal
    else:
        return performance_goal


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


@login_required
def chart_data(request, metric_id, school_id):
    if request.method == "GET":
        a_year_ago = datetime.today() - relativedelta(years=1)
        cy_measures = Measure.objects.filter(
            metric=metric_id, school=school_id, date__range=school_year_range()
        ).order_by("date")
        cy_values = [measure.value for measure in cy_measures]
        py_measures = Measure.objects.filter(
            metric=metric_id,
            school=school_id,
            date__range=school_year_range(a_year_ago),
        ).order_by("date")
        py_values = [measure.value for measure in py_measures]
        py_months = [measure.month_name for measure in py_measures]
        cy_months = [measure.month_name for measure in cy_measures]
        months = list(set(py_months + cy_months))
        months.sort(key=month_order)
        if py_measures:
            py_label = py_measures.first().school_year
        else:
            py_label = None

        if py_values:
            eoy_value = py_values[-1]
        else:
            eoy_value = None
        goal = target(eoy_value, metric_id)

        data = {
            "months": months,
            "py_label": py_label,
            "previous_year": py_values,
            "cy_label": cy_measures.first().school_year,
            "current_year": cy_values,
            "goal": goal,
        }
        return JsonResponse({"success": True, "data": data})
    raise PermissionDenied


@login_required
def high_health(request, school_level=None):
    user = request.user
    if school_level:
        measures = Measure.objects.filter(school__school_level=school_level).order_by(
            "metric__essential_question", "metric", "school"
        )
    else:
        school_level = user.profile.site.school_level
        measures = Measure.objects.filter(school__school_level=school_level)
    schools = set([measure.school for measure in measures])
    school_levels = [
        {"name": "Elementary Schools", "url": "/high_health/1"},
        {"name": "Middle Schools", "url": "/high_health/2"},
        {"name": "High Schools", "url": "/high_health/4"},
        {"name": "K-8 Schools", "url": "/high_health/3"},
    ]
    context = {
        # "measures": measures,
        "schools": schools,
        "metrics": metrics(measures.filter(is_current=True)),
        "school_levels": school_levels,
    }
    return render(request, "high_health.html", context)

