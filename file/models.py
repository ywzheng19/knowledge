from django.db import models
from django.contrib.auth.models import User

# 20210314 新增模型上传文件
class File(models.Model):
    name = models.CharField(max_length=255, verbose_name = '文件名', null=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="上传者")
    upload = models.FileField(upload_to='', verbose_name="上传文件")

    class Meta:
        verbose_name = verbose_name_plural = '文件' 

