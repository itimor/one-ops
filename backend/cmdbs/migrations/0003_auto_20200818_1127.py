# Generated by Django 3.0.3 on 2020-08-18 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdbs', '0002_auto_20200802_1704'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='host',
            name='disk',
        ),
        migrations.AddField(
            model_name='host',
            name='cpu_num',
            field=models.SmallIntegerField(blank=True, null=True, verbose_name='cpu个数'),
        ),
        migrations.AddField(
            model_name='host',
            name='data_disk',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='数据磁盘'),
        ),
        migrations.AddField(
            model_name='host',
            name='datastore',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='数据中心名称'),
        ),
        migrations.AddField(
            model_name='host',
            name='dns',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='dns'),
        ),
        migrations.AddField(
            model_name='host',
            name='netmask',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='子网掩码'),
        ),
        migrations.AddField(
            model_name='host',
            name='other_disk',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='其他磁盘'),
        ),
        migrations.AddField(
            model_name='host',
            name='sys_disk',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='系统磁盘'),
        ),
        migrations.AddField(
            model_name='host',
            name='vcenter',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='所在vcenter地址'),
        ),
        migrations.AlterField(
            model_name='host',
            name='memory',
            field=models.SmallIntegerField(blank=True, default='1', null=True, verbose_name='内存信息'),
        ),
        migrations.AlterField(
            model_name='host',
            name='os',
            field=models.CharField(choices=[(1, 'centos'), (2, 'windows'), (3, 'debian'), (4, 'other')], default=1, max_length=30, verbose_name='操作系统'),
        ),
    ]
