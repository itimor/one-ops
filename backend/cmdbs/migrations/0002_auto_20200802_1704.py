# Generated by Django 3.0.3 on 2020-08-02 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdbs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='status',
            field=models.CharField(choices=[(0, '待初始化'), (1, '已使用'), (2, '未使用'), (3, '待下线'), (4, '已下线')], default=0, max_length=30, verbose_name='设备状态'),
        ),
    ]
