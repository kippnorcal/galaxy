from django.db import models
from django.db.models import Case, When, Value, IntegerField
from django.contrib import admin
from django.contrib.auth.models import User, Group


class TableauPermissionsGroup(models.Model):
    group_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class Role(models.Model):
    name = models.CharField(max_length=100)
    permission_groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class SchoolLevelManager(models.Manager):
    def get_ordered(self):
        """Method to ensure Regional school level is displayed last"""
        qs = self.get_queryset()
        last_id = 5
        qs = qs.annotate(
            custom_order=Case(
                When(id=last_id, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'id')
        return qs


class SchoolLevel(models.Model):
    objects = SchoolLevelManager()
    name = models.CharField(max_length=3)
    display_name = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=100)
    is_school = models.BooleanField(default=True)
    school_level = models.ForeignKey(
        SchoolLevel, on_delete=models.PROTECT, null=True, blank=True
    )
    tableau_permissions = models.ManyToManyField(TableauPermissionsGroup, blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class SiteAdmin(admin.ModelAdmin):
    list_display = ("__str__", "is_active", "is_school", "school_level")
    list_filter = ("is_school", "school_level")


class Job(models.Model):
    name = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, blank=True, null=True)
    tableau_permissions = models.ManyToManyField(TableauPermissionsGroup, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class JobAdmin(admin.ModelAdmin):
    list_display = ("__str__",)
    list_filter = ("role",)
    search_fields = ["name"]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    employee_number = models.CharField(unique=True, max_length=5)
    email = models.EmailField(unique=True)
    job_title = models.ForeignKey(Job, on_delete=models.PROTECT, blank=True, null=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT, blank=True, null=True)
    avatar_url = models.URLField(max_length=2000, blank=True)
    favorites = models.ManyToManyField("catalog.Report", through="catalog.Favorite")
    base_tableau_permissions = models.ManyToManyField(
        TableauPermissionsGroup, blank=True, null=True, related_name="base_permissions"
    )
    tableau_permission_exceptions = models.ManyToManyField(
        TableauPermissionsGroup, blank=True, null=True, related_name="permission_exceptions"
    )
    permission_exceptions_note = models.TextField(blank=True)
    is_contractor = models.BooleanField(default=False, help_text="Denotes if the profile belongs to a contractor."
                                            "If checked, the profile will not be deactivated by the Galaxy connector.")
    contractor_end_date = models.DateField(blank=True, null=True)
    contractor_note = models.TextField(blank=True)

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
        "job_title__name",
        "employee_number",
    ]
