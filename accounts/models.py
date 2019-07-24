from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class SchoolLevel(models.Model):
    name = models.CharField(max_length=2)
    display_name = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=100)
    is_school = models.BooleanField(default=True)
    school_level = models.ForeignKey(
        SchoolLevel, on_delete=models.PROTECT, null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class SiteAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    list_filter = ("is_school", "school_level")


class Job(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True)
    employee_number = models.CharField(max_length=5, blank=True)
    email = models.EmailField()
    job_title = models.ForeignKey(Job, on_delete=models.PROTECT, blank=True, null=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT, blank=True, null=True)
    avatar_url = models.URLField(max_length=2000, blank=True)
    favorites = models.ManyToManyField("catalog.Report", through="catalog.Favorite")

    def __str__(self):
        return self.email

    class Meta:
        ordering = ("user",)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("__str__", "job_title")
    list_filter = ("site", "job_title__role")
    search_fields = [
        "user__first_name",
        "user__last_name",
        "email",
        "job_title",
        "employee_number",
    ]
