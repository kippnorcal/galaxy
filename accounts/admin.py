from django.contrib import admin
from .models import Role, Site
from .models import Profile, ProfileAdmin

admin.site.register(Role)
admin.site.register(Site)
admin.site.register(Profile, ProfileAdmin)
