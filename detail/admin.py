from django.contrib import admin

from .models import Category, Tag, Post, Log
from knowledge.custom_site import custom_site
from .adminforms import PostAdminForm, LogAdminForm

@admin.register(Category, site=custom_site)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'owner', 'created_time')
    fields = ('name', 'status', 'is_nav')   # 增加分类页面显示的字段

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag, site=custom_site)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'owner', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)

@admin.register(Post, site=custom_site)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm    # 20210224自定义form
    list_display = ('title', 'category', 'status', 'pv', 'owner', 'created_time')
    list_display_links = []

    list_filter = ['category', ]
    search_fields = ['title', 'category_name']

    actions_on_bottom = False 

    fields = (
        'is_top',
        ('category', 'title'),
        'desc',
        'status', 
        'content',
        'tag',
    )

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

@admin.register(Log, site=custom_site)
class LogAdmin(admin.ModelAdmin):
    form = LogAdminForm     # 20210314自定义form
    list_display = ('title', 'content')
