from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms.models import ModelChoiceField
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


class ReportManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def for_user(self, user):
        return self.get_queryset().filter(
            roles=user.profile.job_title.role,
            sites=user.profile.site
        )


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

    objects = models.Manager()
    active = ReportManager()

    def __str__(self):
        return self.name

    def host_url(self):
        uri = urlparse(self.url)
        return f"{uri.scheme}://{uri.netloc}/"

    def path(self):
        return urlparse(self.url).fragment

    def embed_name(self):
        # Substring everything after views/
        return self.path().split('views/')[1]

    def site_root(self):
        # Substring between site/ and the next /
        site_root = self.path().split('site/')[1].split('/')[0]
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

    search_fields = ['name', 'category__name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'owner':
            queryset = User.objects.filter(is_staff=True)
            return ModelChoiceField(queryset, initial=request.user)
        else:
            return super(ReportAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}'

    class Meta:
        ordering = ('-timestamp',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'report', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ['user', 'report']


class Feedback(models.Model):
    score = models.IntegerField(validators=[
        MaxValueValidator(5),
        MinValueValidator(1)
    ])
    comment = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.report} -- {self.user.get_full_name()}'

    class Meta:
        ordering = ('report', 'user', 'timestamp',)
        verbose_name_plural = 'feedback'


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'score', 'timestamp',)
    list_filter = ('score', 'report',)
    search_fields = ['report__name', 'user__first_name', 'user__last_name']
