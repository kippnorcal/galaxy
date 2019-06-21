import datetime
from django.db import models
from catalog.models import Report
from accounts.models import Site, SchoolLevel


class EssentialQuestion(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Metric(models.Model):
    def school_level_default():
        return SchoolLevel.objects.all()

    goal_type_choices = [
        ("ABOVE", "above"),
        ("BELOW", "below"),
    ]
    name = models.CharField(max_length=100)
    definition = models.TextField(blank=True)
    essential_question = models.ForeignKey(
        EssentialQuestion,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    school_level = models.ManyToManyField(SchoolLevel, default=school_level_default)
    performance_goal = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    growth_goal = models.IntegerField(default=0)
    goal_type = models.CharField(max_length=5, choices=goal_type_choices, default=goal_type_choices[0][0])
    report = models.ForeignKey(
        Report,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date = models.DateField(default=datetime.date.today)

    @property
    def year(self):
        return self.date.year

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Measure(models.Model):
    metric = models.ForeignKey(Metric, on_delete=models.PROTECT)
    school = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        limit_choices_to={'is_school': True},
    )
    value = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField(default=datetime.date.today)

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
