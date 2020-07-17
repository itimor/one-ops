# -*- coding: utf-8 -*-
# author: itimor

from django.urls import path

from chats.consumers import ChatConsumer

websocket_urlpatterns = [  # 路由，指定 websocket 链接对应的 consumer
    path('ws/chat/<str:room_name>/', ChatConsumer),
]
