from django.contrib import admin
from .models import PageView, PageViewAdmin
from .models import Search, SearchAdmin


admin.site.register(PageView, PageViewAdmin)
admin.site.register(Search, SearchAdmin)
