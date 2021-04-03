import logging
FORMAT = '%(asctime)s-%(name)s-%(funcName)s:%(message)s'
logging.basicConfig(level=logging.debug, format=FORMAT)
import os

from django.shortcuts import render
from django.http import FileResponse

from .models import File
from detail.models import Category
from config.models import SideBar
from detail.views import login_decorator


# 20210314 新增下载页处理方法
@login_decorator
def download(request, down_id=None):
    file_list = File.objects.all()
    context={'file_list': file_list}
    context.update(Category.get_navs())
    context.update(SideBar.get_all())
    if down_id:
        fileobj = File.objects.filter(id=down_id).values('upload')[0]   # 字典{'upload': 文件名} 
        file1 = fileobj.get('upload')   # 文件名 
        file2 = os.path.join('/root/workspace/knowledge/knowledge/upload/', file1)  # 文件绝对路径
        file3 = open(file2, 'rb')   # 打开文件
        response = FileResponse(file3, filename=file1, as_attachment=True)
        return response
    else:
        return render(request, 'detail/download.html', context=context)

