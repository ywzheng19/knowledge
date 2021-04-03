from django.contrib import admin

from .models import SideBar, Link
from knowledge.custom_site import custom_site

@admin.register(SideBar, site=custom_site)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'display_type', 'status', 'owner', 'created_time')
    fields = ('title', 'display_type', 'content')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)


@admin.register(Link, site=custom_site)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'href', 'status', 'weight', 'owner')
    fields = ('title', 'href', 'weight')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)
