# -*- coding: utf-8 -*-
# author: itimor

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from cmdbs.models import *
import subprocess


class CmdConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['cid']
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        cmd = text_data_json['cmd']
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'cmdrun',
                'cmd': cmd
            }
        )

    async def cmdrun(self, event):
        await save_cmd(event)
        cmd = subprocess.Popen(event['cmd'], stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE, universal_newlines=True, shell=True, bufsize=1)
        # 实时输出
        while True:
            line = cmd.stdout.readline()
            print(f'{line}')
            await self.send(text_data=json.dumps({'text': line}))
            if subprocess.Popen.poll(cmd) == 0:  # 判断子进程是否结束
                break


from asgiref.sync import sync_to_async
from cmdbs.serializers import *
from rest_framework.renderers import JSONRenderer
from utils.compatibility import text_


@sync_to_async
def save_cmd(event):
    cmd = event['cmd']
    try:
        obj = History.objects.get(cmd=cmd)
        obj.num += 1
        obj.save()
    except:
        obj = History.objects.create(cmd=cmd, num=1)

    serializer = HistorySerializer(obj)
    j = JSONRenderer().render(serializer.data)
    data = json.loads(text_(j))
    return data

# @sync_to_async
# def get_all_users():
#     return User.objects.all()
#
# async def foo(request):
#     for user in await get_all_users():
#         print(user)