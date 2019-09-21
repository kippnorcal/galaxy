from django import template

register = template.Library()


@register.filter
def goal_format(measure):
    if measure.goal.goal_type == "ABOVE":
        if measure.value <= measure.goal.previous_outcome:
            return "danger"
        elif measure.value < measure.goal.target:
            return "secondary"
        else:
            return "success"
    else:
        if measure.value >= measure.goal.previous_outcome:
            return "danger"
        elif measure.value > measure.goal.target:
            return "secondary"
        else:
            return "success"


@register.filter
def addstr(arg1, arg2):
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def goal_distance(measure):
    if measure.goal.goal_type == "ABOVE":
        if measure.value < measure.goal.target:
            return f"-{measure.goal.target - measure.value}% below goal"
        else:
            return f"+{measure.value - measure.goal.target}% above goal"

    else:
        if measure.value > measure.goal.target:
            return f"+{measure.value - measure.goal.target}% above goal"
        else:
            return f"-{measure.goal.target - measure.value}% below goal"


register.filter("goal_format", goal_format)
register.filter("addstr", addstr)
register.filter("goal_distance", goal_distance)

