from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User


class PageView(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    page = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.page}"

    class Meta:
        ordering = ('-timestamp',)


class PageViewAdmin(admin.ModelAdmin):
    list_filter = ('user', 'page',)
    list_display = ('__str__', 'user', 'timestamp',)


class Search(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
    )
    search_term = models.CharField(max_length=255)
    search_timestamp = models.DateTimeField(auto_now_add=True)
    destination = models.CharField(max_length=255, null=True, blank=True)
    click_through_timestamp = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.search_term}"

    class Meta:
        ordering = ('-search_timestamp',)
        verbose_name_plural = "searches"

class SearchAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'search_timestamp',)
    list_search = ('search_term',)


class Login(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    referrer = models.CharField(max_length=255, null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.timestamp}"

    class Meta:
        ordering = ('-timestamp',)
