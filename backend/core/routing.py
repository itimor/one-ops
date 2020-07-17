# -*- coding: utf-8 -*-
# author: itimor

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from chats.routing import ChatRouting

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    # 普通的HTTP请求不需要我们手动在这里添加，框架会自动加载过来
    'websocket': AuthMiddlewareStack(
        URLRouter(
            ChatRouting
        )
    ),
})
