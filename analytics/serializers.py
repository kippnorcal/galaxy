from .models import PageView, Search, Login
from django.contrib.auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Login
        fields = ("id", "user", "referrer", "user_agent", "ip_address", "timestamp")
        read_only_fields = ("user", "referrer", "user_agent", "ip_address", "timestamp")


class SearchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Search
        fields = (
            "id",
            "user",
            "search_term",
            "search_timestamp",
            "destination",
            "click_through_timestamp",
        )
        read_only_fields = (
            "user",
            "search_term",
            "search_timestamp",
            "destination",
            "click_through_timestamp",
        )


class PageViewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PageView
        fields = ("id", "user", "page", "timestamp")
        read_only_fields = ("user", "page", "timestamp")

