"""knowledge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url

from .custom_site import custom_site
from detail.views import login, logout, post_list, post_detail, search, author, changelog
from file.views import download
from config.views import links

urlpatterns = [
    url(r'^$', post_list, name='index'), # 首页
    url(r'^login/$', login, name='login'), # 登录页 
    url(r'^logout/$', logout, name='logout'), # 注销请求 
    url(r'^category/(?P<category_id>\d+)/$', post_list, name='category-list'), # 分类列表页
    url(r'^tag/(?P<tag_id>\d+)/$', post_list, name='tag-list'), # 标签列表页
    url(r'^post/(?P<post_id>\d+).html$', post_detail, name='post-detail'),   # 知识详情页
    url(r'^search/$', search, name='search'),   # 搜索列表页; 20210303
    url(r'^author/(?P<owner_id>\d+)/$', author, name='author'),   # 作者知识列表页
    url(r'^links/$', links), # 友链页
    url(r'^changelog/$', changelog, name='changelog'),  # 更新日志页; 20210314
    url(r'^download/$', download, name='download'),  # 下载页; 20210314
    url(r'^download/(?P<down_id>\d+)/$', download, name='download-id'),  # 下载功能; 20210314
    url(r'super_admin/', admin.site.urls),  # django默认管理页面
    url(r'admin/', custom_site.urls),   # 自定义管理页面
]
