from django.contrib import admin
from school.models import *



class PublishAdmin(admin.ModelAdmin):
    list_display = ('publisher', 'sex','date', 'time','price','publishDate','other','state','accepter')

admin.site.register(Publish, PublishAdmin)