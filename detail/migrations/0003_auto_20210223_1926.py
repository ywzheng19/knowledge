# Generated by Django 3.1.7 on 2021-02-23 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detail', '0002_post_pv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='pv',
            field=models.PositiveIntegerField(default=0, verbose_name='访问量'),
        ),
    ]