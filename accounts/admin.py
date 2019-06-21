from django.contrib import admin
from .models import Role, Job
from .models import Site, SiteAdmin
from .models import Profile, ProfileAdmin

admin.site.register(Role)
admin.site.register(Site, SiteAdmin)
admin.site.register(Job)
admin.site.register(Profile, ProfileAdmin)
