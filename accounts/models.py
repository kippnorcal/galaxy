from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Site(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Job(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True)
    employee_number =  models.CharField(max_length=5, blank=True)
    email = models.EmailField()
    job_title = models.ForeignKey(Job, on_delete=models.PROTECT, blank=True, null=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT, blank=True, null=True)
    avatar_url = models.URLField(max_length=2000, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ('user',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'job_title')
    list_filter = ('site', 'job_title__role')
    search_fields = [
        'user__first_name',
        'user__last_name',
        'email',
        'job_title',
        'employee_number'
    ]
