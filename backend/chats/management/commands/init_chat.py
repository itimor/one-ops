# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from systems.models import *
from systems.menus import init_menu


class Command(BaseCommand):

    def handle(self, *args, **options):
        topmenu = Menu.objects.get(name='top', code='top')
        self.stdout.write(self.style.SUCCESS('############ 初始化聊天菜单 ###########'))
        basemenu = Menu.objects.create(name='聊天管理', code='chat', curl='/chat', icon='chat', sequence=4, type=1,
                                         parent=topmenu)
        menumodel = Menu.objects.create(name='群组管理', code='chatgroup', curl='/chatgroup', icon='group', sequence=10, type=2,
                                        parent=basemenu)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='消息管理', code='chatmessage', curl='/chatmessage', icon='message',
                                        sequence=20, type=2, parent=basemenu)
        init_menu(menumodel)
        menumodel = Menu.objects.create(name='聊天室', code='chatroom', curl='/chatroom', icon='chatroom',
                                        sequence=30, type=2, parent=basemenu)
        init_menu(menumodel)
        self.stdout.write(self.style.SUCCESS('初始化完成'))
