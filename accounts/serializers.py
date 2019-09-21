from .models import Role, SchoolLevel, Site, Job, Profile
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "is_active", "is_staff")
        read_only_fields = ("email", "username", "is_staff")


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")


class JobSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    class Meta:
        model = Job
        fields = ("id", "name", "role")


class SchoolLevelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SchoolLevel
        fields = ("id", "name", "display_name")


class SiteSerializer(serializers.HyperlinkedModelSerializer):
    school_level = serializers.PrimaryKeyRelatedField(
        queryset=SchoolLevel.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Site
        fields = ("id", "name", "is_school", "school_level")


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    job_title = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Profile
        fields = ("id", "employee_number", "email", "job_title", "site", "user")
