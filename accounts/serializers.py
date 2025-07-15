from .models import Role, SchoolLevel, Site, Job, Profile, TableauPermissionsGroup
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "is_active",
            "is_staff",
            "last_login",
            "date_joined"
        )
        read_only_fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "username",
            "is_staff",
            "last_login",
            "date_joined")


class TableauPermissionsGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TableauPermissionsGroup
        fields = (
            "id",
            "group_id",
            "name",
            "is_active"
        )


class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ("id", "name")


class JobSerializer(serializers.HyperlinkedModelSerializer):
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False, allow_null=True)
    tableau_permissions = serializers.PrimaryKeyRelatedField(
        queryset=TableauPermissionsGroup.objects.all(), many=True, required=False
    )

    class Meta:
        model = Job
        fields = ("id", "name", "role", "tableau_permissions")

    def validate_name(self, value):
        if Job.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(f'Job with name "{value}" already exists.')
        return value


class SchoolLevelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SchoolLevel
        fields = ("id", "name", "display_name")


class SiteSerializer(serializers.HyperlinkedModelSerializer):
    school_level = serializers.PrimaryKeyRelatedField(
        queryset=SchoolLevel.objects.all(), required=False, allow_null=True
    )
    tableau_permissions = serializers.PrimaryKeyRelatedField(
        queryset=TableauPermissionsGroup.objects.all(), many=True, required=False
    )

    class Meta:
        model = Site
        fields = ("id", "name", "is_school", "school_level", "tableau_permissions")


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    job_title = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all(), required=False, allow_null=True)
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all(), required=False, allow_null=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )
    tableau_permission_exceptions = serializers.PrimaryKeyRelatedField(
        queryset=TableauPermissionsGroup.objects.all(), many=True, required=False, allow_null=True
    )
    base_tableau_permissions = serializers.PrimaryKeyRelatedField(
        queryset=TableauPermissionsGroup.objects.all(), many=True, required=False, allow_null=True
    )

    class Meta:
        model = Profile
        fields = (
            "id",
            "employee_number",
            "first_name",
            "last_name",
            "nickname",
            "email",
            "job_title",
            "site",
            "user",
            "base_tableau_permissions",
            "tableau_permission_exceptions"
        )
