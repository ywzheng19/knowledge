from django.contrib.admin import AdminSite


class CustomSite(AdminSite):
    site_header = '东亚技术知识库'
    site_title = '东亚技术知识库管理后台'
    index_title = '首页'

custom_site = CustomSite(name='cus_admin')
