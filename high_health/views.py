from itertools import chain, groupby
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
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

@login_required
def high_health(request, school_level=None):
    user = request.user
    if school_level:
        measures = Measure.objects.filter(school__school_level=school_level).order_by('metric__essential_question', 'metric', 'school')
    else:
        school_level = user.profile.site.school_level
        measures = Measure.objects.filter(school__school_level=school_level)
    schools = set([ measure.school for measure in measures])
    school_levels = [
        {"name":"Elementary Schools","url":"/high_health/1"},
        {"name":"Middle Schools","url":"/high_health/2"},
        {"name":"High Schools","url":"/high_health/4"},
        {"name":"K-8 Schools","url":"/high_health/3"},
    ]
    context = {
        'measures': measures,
        'schools': schools,
        'metrics': metrics(measures),
        'school_levels': school_levels,
    }
    return render(request, "high_health.html", context)


