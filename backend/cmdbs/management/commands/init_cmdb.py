# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *
from systems.menus import init_menu


class Command(BaseCommand):

    def handle(self, *args, **options):
        topmenu = Menu.objects.get(name='top', code='top')
        self.stdout.write(self.style.SUCCESS('############ 初始化cmdb菜单 ###########'))
        basemenu = Menu.objects.create(name='cmdbs', code='cmdbs', curl='/cmdbs', icon='cmdbs', sequence=5, type=1,
                                       parent=topmenu)
        menumodel = Menu.objects.create(name='机房', code='idc', curl='/idc', icon='idc', sequence=10, type=2,
                                        parent=basemenu)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='主机组', code='hostgroup', curl='/hostgroup', icon='hostgroup', sequence=20, type=2,
                                        parent=basemenu)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='主机', code='host', curl='/host', icon='host', sequence=30, type=2,
                                        parent=basemenu)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='执行命令', code='shell', curl='/shell', icon='shell',
                                        sequence=40, type=2, parent=basemenu)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='历史命令', code='history', curl='/history', icon='history', sequence=50, type=2,
                                        parent=basemenu)
        init_menu(menumodel)
        self.stdout.write(self.style.SUCCESS('初始化完成'))
