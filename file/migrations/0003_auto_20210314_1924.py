# Generated by Django 3.1.7 on 2021-03-14 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0002_auto_20210314_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='upload',
            field=models.FileField(upload_to='', verbose_name='上传文件'),
        ),
    ]