from django.contrib import admin
from website.models import Site, UserRecords,Job

admin.site.register(Site)
admin.site.register(UserRecords)
admin.site.register(Job)