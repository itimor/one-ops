# -*- coding: utf-8 -*-
# author: itimor

from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from chats.consumers import ChatConsumer

application = ProtocolTypeRouter({
    # Empty for now (http->django views is added by default)
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    # int_path
                    # re_path(r'^chat/(?P<room_name>[0-9]{1,4})/$', ChatConsumer),
                    # str_path
                    re_path(r'^chat/(?P<room_name>[\w-]+)', ChatConsumer),
                ]
            )
        )
    )
})
