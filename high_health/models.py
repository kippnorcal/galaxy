from django.db import models
from catalog.models import Report
from accounts.models import Site


class EssentialQuestion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Metric(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    essential_question = models.ForeignKey(EssentialQuestion, on_delete=models.PROTECT, null=True, blank=True)
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class SchoolLevel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class School(models.Model):
    name = models.CharField(max_length=100)
    school_level = models.ForeignKey(SchoolLevel, on_delete=models.PROTECT, null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Goal(models.Model):
    goal_type_choices = [
        ("ABOVE", "above"),
        ("BELOW", "below"),
    ]
    goal_type = models.CharField(max_length=5, choices=goal_type_choices)
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    @property
    def year(self):
        return self.date.year

    def __str__(self):
        return f"{self.year} {self.school}: {self.metric}"

    class Meta:
        ordering = ['-date', 'school', 'metric',]


class Measure(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    school = models.ForeignKey(School, on_delete=models.PROTECT)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    goal = models.ForeignKey(Goal, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    @property
    def year(self):
        return self.date.year

    @property
    def month(self):
        return self.date.month

    def __str__(self):
        return f"{self.year}-{self.month} {self.school}: {self.metric}"

    class Meta:
        ordering = ['-date', 'school', 'metric']
