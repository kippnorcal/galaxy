import logging
from typing import Union

from django import template
from high_health.models import Measure

register = template.Library()


logger = logging.getLogger('console')


@register.filter
def goal_format(measure: Measure) -> str:
    # This method creates a tag that determines the color of the text
    # Color codings found in css file
    if measure.metric.frequency == "MoM":
        current_month = measure.month
        last_year = measure.year - 1
        try:
            previous_outcome = Measure.objects.filter(
                metric=measure.metric.id,
                date__month=current_month,
                date__year=last_year,
                school=measure.school)[0].value
        except IndexError:
            previous_outcome = measure.goal.previous_outcome
        if previous_outcome is None:
            previous_outcome = measure.goal.previous_outcome
        return mom_color_eval(measure, previous_outcome)
    else:
        previous_outcome = measure.goal.previous_outcome
        return yoy_color_eval(measure, previous_outcome)


def yoy_color_eval(measure: Measure, previous: Union[int, None]) -> str:
    if measure.goal.goal_type.upper() == "ABOVE":
        if measure.value >= measure.goal.target:
            return "success"
        elif measure.goal.target > measure.value >= previous:
            return "secondary"
        else:
            return "danger"
    else:
        if measure.value <= measure.goal.target:
            return "success"
        elif measure.goal.target < measure.value <= previous:
            return "secondary"
        else:
            return "danger"


def mom_color_eval(measure, previous):
    # Filtering the % Staffed metric out of evaluation
    if measure.metric.id == 36:
        return "secondary"

    if measure.goal.goal_type.upper() == "ABOVE":
        if measure.value < previous:
            return "danger"
        elif measure.value >= measure.goal.target and measure.value >= previous:
            return "success"
        else:
            return "secondary"
    else:
        if measure.value > previous:
            return "danger"
        elif measure.value <= measure.goal.target and measure.value <= previous:
            return "success"
        else:
            return "secondary"


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
