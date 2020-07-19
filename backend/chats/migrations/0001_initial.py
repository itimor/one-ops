# Generated by Django 3.0.3 on 2020-07-19 04:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='名称')),
                ('code', models.CharField(max_length=32, unique=True, verbose_name='代码')),
                ('create_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='create_user', to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('join_user', models.ManyToManyField(related_name='join_user', to=settings.AUTH_USER_MODEL, verbose_name='群员')),
            ],
            options={
                'verbose_name': '群组',
                'verbose_name_plural': '群组',
            },
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
                ('message', models.TextField(verbose_name='消息内容')),
                ('create_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='创建者')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chats.ChatGroup', verbose_name='群组')),
            ],
            options={
                'verbose_name': '消息',
                'verbose_name_plural': '消息',
            },
        ),
    ]
