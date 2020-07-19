# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url
from rest_framework import routers
from chats.views import ChatGroupViewSet, ChatMessageViewSet

router = routers.DefaultRouter()

router.register(r'chatgroup', ChatGroupViewSet)
router.register(r'chatmesage', ChatMessageViewSet)

urlpatterns = [
]

urlpatterns += router.urls
