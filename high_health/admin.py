from django.contrib import admin
from .models import EssentialQuestion, Goal, Metric, Measure
from .models import GoalAdmin, MetricAdmin, MeasureAdmin


admin.site.register(EssentialQuestion)
admin.site.register(Metric, MetricAdmin)
admin.site.register(Measure, MeasureAdmin)
admin.site.register(Goal, GoalAdmin)
