# -*- coding: utf-8 -*-
# author: itimor

from chats.serializers import *
from common.views import ModelViewSet, BulkModelMixin


class ChatGroupViewSet(BulkModelMixin):
    queryset = ChatGroup.objects.all()
    serializer_class = ChatGroupSerializer
    search_fields = ['name']
    filter_fields = ['name', 'create_user', 'join_user']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return ChatGroupReadSerializer
        return ChatGroupSerializer


class ChatMessageViewSet(BulkModelMixin):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    search_fields = ['message']
    filter_fields = ['create_user']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return ChatMessageReadSerializer
        return ChatMessageSerializer
