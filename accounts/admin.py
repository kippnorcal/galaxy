from django.contrib import admin
from .models import Role, SchoolLevel
from .models import Job, JobAdmin
from .models import Site, SiteAdmin
from .models import Profile, ProfileAdmin

admin.site.register(Role)
admin.site.register(Site, SiteAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(SchoolLevel)
