# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *
from systems.menus import init_menu


class Command(BaseCommand):

    def handle(self, *args, **options):
        topmenu = Menu.objects.get(name='top', code='top')
        self.stdout.write(self.style.SUCCESS('############ 初始化jenkins菜单 ###########'))
        basemenu = Menu.objects.create(name='jenkins任务', code='jenkins', curl='/jenkins', icon='jenkins', sequence=2, type=1,
                                       parent=topmenu)
        menumodel = Menu.objects.create(name='任务', code='task', curl='/task', icon='task', sequence=10, type=2,
                                        parent=basemenu)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='任务日志', code='tasklog', curl='/tasklog', icon='tasklog', sequence=20, type=2,
                                        parent=basemenu)
        init_menu(menumodel)
        Menu.objects.create(name='ping测试', code='ping', curl='/ping', icon='ping', sequence=30, type=2,
                            hidden=True, active_menu='/task', parent=basemenu)
        Menu.objects.create(name='创建机器', code='createvm', curl='/createvm', icon='createvm', sequence=40, type=2,
                            hidden=True, active_menu='/task', parent=basemenu)
        Menu.objects.create(name='初始化主机', code='initvm', curl='/initvm', icon='initvm', sequence=50, type=2,
                            hidden=True, active_menu='/task', parent=basemenu)
        Menu.objects.create(name='下线主机', code='destoryvm', curl='/destoryvm', icon='destoryvm', sequence=60, type=2,
                            hidden=True, active_menu='/task', parent=basemenu)
        self.stdout.write(self.style.SUCCESS('初始化完成'))
