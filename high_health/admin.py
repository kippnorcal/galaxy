from django.contrib import admin
from .models import EssentialQuestion, Metric, Measure
from .models import MetricAdmin, MeasureAdmin


admin.site.register(EssentialQuestion)
admin.site.register(Metric, MetricAdmin)
admin.site.register(Measure, MeasureAdmin)
