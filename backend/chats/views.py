# -*- coding: utf-8 -*-
# author: itimor

from chats.serializers import *
from common.views import ModelViewSet, BulkModelMixin


class ChatGroupViewSet(BulkModelMixin):
    queryset = ChatGroup.objects.all()
    serializer_class = ChatGroupSerializer
    filter_fields = ['namae']


class ChatMessageViewSet(BulkModelMixin):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    filter_fields = ['message']
