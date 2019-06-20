from django.contrib import admin
from .models import EssentialQuestion, Metric
from .models import SchoolLevel, School
from .models import Goal, Measure


admin.site.register(EssentialQuestion)
admin.site.register(Metric)
admin.site.register(SchoolLevel)
admin.site.register(School)
admin.site.register(Goal)
admin.site.register(Measure)
