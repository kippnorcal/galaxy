from django.db import models
from django.contrib import admin


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)


class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)
