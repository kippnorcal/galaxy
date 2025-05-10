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
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    tableau_permissions = TableauPermissionsGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = ("id", "name", "role", "tableau_permissions")


class SchoolLevelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SchoolLevel
        fields = ("id", "name", "display_name")


class SiteSerializer(serializers.HyperlinkedModelSerializer):
    school_level = serializers.PrimaryKeyRelatedField(
        queryset=SchoolLevel.objects.all(), required=False, allow_null=True
    )
    tableau_permissions = TableauPermissionsGroupSerializer(many=True, read_only=True)

    class Meta:
        model = Site
        fields = ("id", "name", "is_school", "school_level", "tableau_permissions")


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    job_title = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    site = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all())
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False, allow_null=True
    )
    base_tableau_permissions = TableauPermissionsGroupSerializer(many=True, required=False)
    tableau_permission_exceptions = TableauPermissionsGroupSerializer(many=True, read_only=True)

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

    def update(self, instance, validated_data):
        # Extract nested base_tableau_permissions
        base_perms_data = validated_data.pop('base_tableau_permissions', None)

        # Update regular fields
        instance = super().update(instance, validated_data)

        # Manually set the M2M relationship
        if base_perms_data is not None:
            # Expecting list of dicts like: [{"id": 1, "name": "Analyst"}, ...]
            group_ids = [item['id'] for item in base_perms_data if 'id' in item]
            instance.base_tableau_permissions.set(group_ids)

        return instance
