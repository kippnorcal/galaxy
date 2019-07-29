from django import template

register = template.Library()


@register.filter
def goal_format(measure):
    if measure.goal.goal_type == "ABOVE":
        if measure.value < measure.goal.target:
            return "danger"
        else:
            return "success"
    else:
        if measure.value <= measure.goal.target:
            return "success"
        else:
            return "danger"


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def perf_goal_format(value, metric):
    if metric.goal_type == "ABOVE":
        if value < metric.performance_goal:
            return "danger"
        else:
            return "success"
    else:
        if value <= metric.performance_goal:
            return "success"
        else:
            return "danger"


register.filter("goal_format", goal_format)
register.filter("addstr", addstr)
register.filter("perf_goal_format", perf_goal_format)

