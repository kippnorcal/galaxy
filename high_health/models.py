from django.db import models
from catalog.models import Report

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
    essential_question = models.ForeignKey(EssentialQuestion, on_delete=models.PROTECT, null=True)
    report = models.ForeignKey(Report, on_delete=models.SET_NULL, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
