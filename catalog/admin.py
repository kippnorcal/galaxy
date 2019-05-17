from django.contrib import admin
from .models import Category, CategoryAdmin
from .models import SubCategory, SubCategoryAdmin
from .models import Report, ReportAdmin

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Report, ReportAdmin)

