from .models import Category, SubCategory, Report, Favorite, Feedback, PublicStat
from accounts.models import Role, Site, Profile, TableauPermissionsGroup
from django.contrib.auth.models import User
from rest_framework import serializers


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = SubCategory
        fields = ("id", "name", "category")


class ReportSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())
    roles = serializers.PrimaryKeyRelatedField(many=True, queryset=Role.objects.all())
    tableau_permissions_groups = serializers.PrimaryKeyRelatedField(many=True, queryset=TableauPermissionsGroup.objects.all())
    sites = serializers.PrimaryKeyRelatedField(many=True, queryset=Site.objects.all())
    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_staff=True)
    )

    class Meta:
        model = Report
        fields = (
            "id",
            "name",
            "url",
            "category",
            "subcategory",
            "roles",
            "tableau_permissions_groups",
            "sites",
            "is_active",
            "is_embedded",
            "height",
            "owner",
        )


class FavoriteSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    report = serializers.PrimaryKeyRelatedField(queryset=Report.objects.all())

    class Meta:
        model = Favorite
        fields = ("id", "profile", "report", "timestamp")
        read_only_fields = ("id", "profile", "report", "timestamp")


class FeedbackSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    report = serializers.PrimaryKeyRelatedField(queryset=Report.objects.all())

    class Meta:
        model = Feedback
        fields = ("id", "score", "comment", "user", "report", "timestamp")
        read_only_fields = ("id", "score", "comment", "user", "report", "timestamp")
