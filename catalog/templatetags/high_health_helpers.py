from django import template

register = template.Library()


@register.filter
def goal_format(measure):
    if measure is None:
        return "muted"
    else:
        if measure.metric.goal_type == "ABOVE":
            if measure.value < (float(measure.metric.performance_goal) - (measure.metric.growth_goal/2)):
                return "danger"
            elif measure.value < measure.metric.performance_goal:
                return "secondary"
            else:
                return "success"
        else:
            if measure.value <= (float(measure.metric.performance_goal) - (measure.metric.growth_goal/2)):
                return "secondary"
            elif measure.value <= measure.metric.performance_goal:
                return "success"
            else:
                return "danger"

register.filter('goal_format', goal_format)
