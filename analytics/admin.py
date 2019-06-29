from django.contrib import admin
from .models import PageView, PageViewAdmin


admin.site.register(PageView, PageViewAdmin)
