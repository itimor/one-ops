# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *
from systems.menus import init_menu


class Command(BaseCommand):

    def handle(self, *args, **options):
        topmenu = Menu.objects.get(name='top', code='top')
        self.stdout.write(self.style.SUCCESS('############ 初始化jenkins菜单 ###########'))
        basemenu = Menu.objects.create(name='job管理', code='job', curl='/job', icon='job', sequence=2, type=1,
                                         parent=topmenu)
        menumodel = Menu.objects.create(name='任务', code='task', curl='/task', icon='task', sequence=10, type=2,
                                        parent=basemenu)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='任务日志', code='tasklog', curl='/tasklog', icon='tasklog', sequence=10, type=2,
                                        parent=basemenu)
        init_menu(menumodel)
        self.stdout.write(self.style.SUCCESS('初始化完成'))
