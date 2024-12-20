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
        previous_outcome = get_mom_previous_outcome(measure)
        return mom_color_eval(measure, previous_outcome)
    else:
        previous_outcome = measure.goal.previous_outcome
        return yoy_color_eval(measure, previous_outcome)


def yoy_color_eval(measure: Measure, previous: Union[int, None]) -> str:
    if measure.goal.goal_type.upper() == "ABOVE":
        if measure.value >= measure.goal.target:
            return "success"
        elif previous is None:
            return "secondary"
        elif measure.goal.target > measure.value >= previous:
            return "secondary"
        else:
            return "danger"
    elif measure.goal.goal_type.upper() != "ABOVE":
        if measure.value <= measure.goal.target:
            return "success"
        elif previous is None:
            return "secondary"
        elif measure.goal.target < measure.value <= previous:
            return "secondary"
        else:
            return "danger"


def get_mom_previous_outcome(measure: Measure) -> Union[int, None]:
    current_month = measure.month
    last_year = measure.year - 1
    try:
        previous_outcome = Measure.objects.filter(
            metric=measure.metric.id,
            date__month=current_month,
            date__year=last_year,
            school=measure.school)[0].value
    except IndexError:
        previous_outcome = None
    return previous_outcome


def mom_color_eval(measure, previous: Union[int, None]) -> str:
    # Filtering the % Staffed metric out of evaluation
    if measure.goal.goal_type.upper() == "ABOVE":
        if previous is None:
            if measure.value >= measure.goal.target:
                return "success"
            else:
                return "secondary"
        elif measure.value < previous:
            return "danger"
        elif measure.value >= measure.goal.target and measure.value >= previous:
            return "success"
        else:
            return "secondary"
    else:
        if previous is None:
            if measure.value >= measure.goal.target:
                return "success"
            else:
                return "secondary"
        elif measure.value > previous:
            return "danger"
        elif measure.value <= measure.goal.target and measure.value <= previous:
            return "success"
        else:
            return "secondary"


@register.filter
def addstr(arg1: str, arg2: str) -> str:
    """concatenate arg1 & arg2"""
    return str(arg1) + str(arg2)


@register.filter
def goal_distance(measure: Measure) -> str:
    if measure.goal is not None:
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
    else:
        return "No goal set for this metric."


register.filter("goal_format", goal_format)
register.filter("addstr", addstr)
register.filter("goal_distance", goal_distance)
