from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from urllib.parse import urlparse
from accounts.models import Role, Site


class Category(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "categories"


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
        verbose_name_plural = "subcategories"


class SubCategoryAdmin(admin.ModelAdmin):
    list_filter = ('is_active',)


class Report(models.Model):
    def roles_default():
        return Role.objects.all()

    def sites_default():
        return Site.objects.all()

    name = models.CharField(max_length=255)
    url = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT, blank=True)
    description= models.TextField(blank=True)
    roles = models.ManyToManyField(Role, default=roles_default)
    sites = models.ManyToManyField(Site, default=sites_default)
    is_active = models.BooleanField(default=True)
    is_embedded = models.BooleanField(default=True)
    owner = models.ForeignKey(
	User,
	on_delete=models.PROTECT,
	null=True,
	limit_choices_to={'is_staff': True}
    )

    def __str__(self):
        return self.name

    def host_url(self):
        uri = urlparse(self.url)
        return f"{uri.scheme}://{uri.netloc}/"

    def path(self):
        return urlparse(self.url).fragment

    def embed_name(self):
        # Substring everything after views/
        return self.path.split('views/')[1]

    def site_root(self):
        # Substring between site/ and the next /
        site_root = self.path.split('site/')[1].split('/')[0]
        return f"/t/{site_root}"


    class Meta:
        ordering = ('name',)

class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'is_embedded',)
    list_filter = (
        'is_active',
        'is_embedded',
        'roles',
        'sites',
        'category',
        'subcategory',
    )
