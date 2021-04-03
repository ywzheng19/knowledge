from django.contrib import admin

from .models import File
from knowledge.custom_site import custom_site


@admin.register(File, site=custom_site)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'upload', 'owner')
    fields = ('name',
            'upload')
    
    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(FileAdmin, self).save_model(request, obj, form, change)
