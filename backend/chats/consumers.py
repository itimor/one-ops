# -*- coding: utf-8 -*-
# author: itimor

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chats.models import *


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

        await self.send(text_data=json.dumps({
            'message': "connect chat success!",
            'group_name': f"{self.room_name}"
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        await self.close()

    async def receive(self, text_data):
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
        user_id = event['user_id']
        group_id = event['group_id']
        message = event['message']

        await save_message(event)
        await self.send(text_data=json.dumps({
            'message': message
        }))


from asgiref.sync import sync_to_async


@sync_to_async
def save_message(event):
    user_id = event['user_id']
    group_id = event['group_id']
    message = event['message']
    obj = ChatMessage.objects.create(create_user_id=user_id, group_id=group_id, message=message)
    return obj
