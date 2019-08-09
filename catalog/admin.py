from django.contrib import admin
from .models import Category, CategoryAdmin
from .models import SubCategory, SubCategoryAdmin
from .models import Report, ReportAdmin
from .models import Favorite, FavoriteAdmin
from .models import Feedback, FeedbackAdmin
from .models import PublicStat

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(PublicStat)

