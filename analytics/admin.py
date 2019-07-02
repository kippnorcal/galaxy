from django.contrib import admin
from .models import PageView, PageViewAdmin
from .models import Search, SearchAdmin
from .models import Login


admin.site.register(PageView, PageViewAdmin)
admin.site.register(Search, SearchAdmin)
admin.site.register(Login)
