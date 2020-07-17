# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *
from systems.menus import init_menu
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = '初始化 菜单 角色 用户 用户组'

    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('############ 初始化角色 ###########'))
            role = Role.objects.create(name='top', code='top', sequence=0, parent=None)
        except Exception as e:
            print(e)
            raise CommandError('初始化角色失败')

        try:
            self.stdout.write(self.style.SUCCESS('############ 初始化用户组 ###########'))
            group = Group.objects.create(name='top', code='top', sequence=0, parent=None)
            group.roles.add(role)
        except:
            raise CommandError('初始化用户组失败')

        try:
            self.stdout.write(self.style.SUCCESS('############ 初始化用户 ###########'))
            user = User.objects.create(username='admin', password=make_password("123456"), group=group, is_admin=True)
            user.roles.add(role)
        except:
            raise CommandError('初始化用户失败')

        menus = Menu.objects.all()
        if len(menus) == 0:
            topmenu = Menu.objects.create(name='top', code='top', curl='/top', icon='top', sequence=0, type=1, parent=None)
            self.stdout.write(self.style.SUCCESS('############ 初始化系统菜单 ###########'))
            sysmenu = Menu.objects.create(name='系统管理', code='sys', curl='/sys', icon='sys', sequence=1, type=1, parent=topmenu)
            menumodel = Menu.objects.create(name='角色管理', code='role', curl='/role', icon='role', sequence=30, type=2, parent=sysmenu)
            init_menu(menumodel)
            menumodel = Menu.objects.create(name='分组管理', code='group', curl='/group', icon='group', sequence=10, type=2, parent=sysmenu)
            init_menu(menumodel)
            menumodel = Menu.objects.create(name='用户管理', code='user', curl='/user', icon='user', sequence=20, type=2, parent=sysmenu)
            init_menu(menumodel)
            menumodel = Menu.objects.create(name='菜单管理', code='menu', curl='/menu', icon='menu', sequence=40, type=2, parent=sysmenu)
            init_menu(menumodel)
            menumodel = Menu.objects.create(name='图标管理', code='icon', curl='/icon', icon='icon', sequence=50, type=2, parent=sysmenu)
            init_menu(menumodel)

            self.stdout.write(self.style.SUCCESS('############ 初始化工具菜单 ###########'))
            toolmenu = Menu.objects.create(name='工具管理', code='tool', curl='/tool', icon='tool', sequence=2, type=1, parent=topmenu)
            menumodel = Menu.objects.create(name='审计日志', code='audit', curl='/audit', icon='audit', sequence=10, type=2, parent=toolmenu)
            init_menu(menumodel)
            menumodel = Menu.objects.create(name='测试页面', code='test', curl='/test', icon='list', sequence=20, type=2, parent=toolmenu)
            init_menu(menumodel)

            self.stdout.write(self.style.SUCCESS('############ 初始化通知菜单 ###########'))
            noticemenu = Menu.objects.create(name='通知管理', code='notice', curl='/notice', icon='notice', sequence=3, type=1, parent=topmenu)
            menumodel = Menu.objects.create(name='邮箱通知', code='mail', curl='/mail', icon='mail', sequence=10, type=2, parent=noticemenu)
            init_menu(menumodel)
            menumodel = Menu.objects.create(name='telegram通知', code='telegram', curl='/telegram', icon='telegram', sequence=20, type=2, parent=noticemenu)
            init_menu(menumodel)

        self.stdout.write(self.style.SUCCESS('初始化完成'))
