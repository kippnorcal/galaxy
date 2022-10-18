import logging

from django import template

register = template.Library()


logger = logging.getLogger('django')


@register.filter
def goal_format(measure):
    # This method creates a tag that determines the color of the text
    # Color codings found in css file
    # For now, success is grey
    if measure.goal.goal_type.upper() == "ABOVE":
        if measure.value >= measure.goal.target:
            return "success"
        elif measure.value >= measure.goal.previous_outcome:
            return "secondary"
        else:
            return "danger"
    else:
        if measure.value <= measure.goal.target:
            return "success"
        # elif measure.value <= measure.goal.previous_outcome:
        #    return "secondary"
        else:
            return "danger"


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
