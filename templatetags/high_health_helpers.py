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
def agg_goal_format(measure):
    if measure["goal"]["goal_type"] == "ABOVE":
        if measure["value"] < measure["goal"]["avg_goal"]:
            return "danger"
        else:
            return "success"
    else:
        if measure["value"] <= measure["goal"]["avg_goal"]:
            return "success"
        else:
            return "danger"


register.filter("goal_format", goal_format)
register.filter("addstr", addstr)
register.filter("agg_goal_format", agg_goal_format)

