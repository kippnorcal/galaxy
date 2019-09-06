import datetime
import calendar
from django.db import models
from django.contrib import admin
from catalog.models import Report
from accounts.models import Site, SchoolLevel


class EssentialQuestion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Metric(models.Model):
    name = models.CharField(max_length=100)
    definition = models.TextField(blank=True)
    essential_question = models.ForeignKey(
        EssentialQuestion, on_delete=models.PROTECT, null=True, blank=True
    )
    frequency_choices = [("MoM", "month over month"), ("YoY", "year over year")]
    frequency = models.CharField(
        max_length=3, choices=frequency_choices, default=frequency_choices[0][0]
    )
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=datetime.date.today)

    @property
    def year(self):
        return self.date.year

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class MetricAdmin(admin.ModelAdmin):
    list_display = ("__str__", "year")
    list_filter = ("essential_question", "date")


class Measure(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    school = models.ForeignKey(
        Site, on_delete=models.PROTECT, limit_choices_to={"is_school": True}
    )
    value = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(default=datetime.date.today)
    is_current = models.BooleanField(default=True)

    @property
    def year(self):
        return self.date.year

    @property
    def school_year(self):
        year = int(self.date.strftime("%y"))
        if self.date.month >= 7 and self.date.month < 12:
            return f"{year}-{year+1}"
        else:
            return f"{year-1}-{year}"

    @property
    def month(self):
        return self.date.month

    @property
    def month_name(self):
        return calendar.month_abbr[self.date.month]

    @property
    def goal(self):
        return Goal.objects.get(school=self.school, metric=self.metric)

    def __str__(self):
        return f"{self.year}-{self.month} {self.school}: {self.metric}"

    class Meta:
        ordering = ["-date", "school", "metric"]


class MeasureAdmin(admin.ModelAdmin):
    list_display = ("__str__", "value", "is_current")
    list_filter = ("metric", "school", "is_current", "date")


class Goal(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE)
    school = models.ForeignKey(
        Site, on_delete=models.SET_NULL, null=True, limit_choices_to={"is_school": True}
    )
    goal_type_choices = [("ABOVE", "above"), ("BELOW", "below")]
    goal_type = models.CharField(
        max_length=5, choices=goal_type_choices, default=goal_type_choices[0][0]
    )
    target = models.DecimalField(max_digits=5, decimal_places=2, default=100)

    def __str__(self):
        return f"{self.school} - {self.metric}"

    class Meta:
        ordering = ["metric", "school__school_level", "school"]


class GoalAdmin(admin.ModelAdmin):
    list_display = ("__str__", "target")
    list_filter = ("metric", "school__school_level", "school")

