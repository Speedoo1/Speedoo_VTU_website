from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(historydata)
admin.site.register(profile)
admin.site.register(waecprice)
admin.site.register(datanetwork)
admin.site.register(
    [airteldataplan, mtndataplan, glodataplan, mobile9dataplan, Dstpackages, GOtvpackages, Startimespackages, ])


# class ChoreAdmin(admin.ModelAdmin):
#     list_display = ('profile', 'waecprice', 'mtndataplan')
#     list_editable = ('profile', 'waecprice', 'mtndataplan')
