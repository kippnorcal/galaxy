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
