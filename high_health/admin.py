from django.contrib import admin
from .models import EssentialQuestion, Metric, Measure


admin.site.register(EssentialQuestion)
admin.site.register(Metric)
admin.site.register(Measure)
