# -*- coding: utf-8 -*-
# author: itimor

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chats.models import *


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        await self.close()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        try:
            heart = text_data_json['heart']
            print('这是一段心跳 %s' % heart)
        except:
            text_data_json = json.loads(text_data)
            user_id = text_data_json['user_id']
            group_id = text_data_json['group_id']
            message = text_data_json['message']
            await self.channel_layer.group_send(
                self.room_name,
                {
                    'type': 'chat_message',
                    'user_id': user_id,
                    'group_id': group_id,
                    'message': message
                }
            )

    async def chat_message(self, event):
        obj = await save_message(event)
        await self.send(text_data=json.dumps(obj))


from asgiref.sync import sync_to_async
from chats.serializers import *
from utils.compatibility import text_
from rest_framework.renderers import JSONRenderer


@sync_to_async
def save_message(event):
    user_id = event['user_id']
    group_id = event['group_id']
    message = event['message']
    obj = ChatMessage.objects.create(create_user_id=user_id, group_id=group_id, message=message)
    print(obj)
    serializer = ChatMessageReadSerializer(obj)
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
