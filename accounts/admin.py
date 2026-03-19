from django.contrib import admin
from .models import SchoolLevel
from .models import Job, JobAdmin
from .models import Site, SiteAdmin
from .models import Profile, ProfileAdmin
from .models import TableauPermissionsGroup

admin.site.register(Site, SiteAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(SchoolLevel)
admin.site.register(TableauPermissionsGroup)
