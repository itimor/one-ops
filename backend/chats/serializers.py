# -*- coding: utf-8 -*-
# author: itimor

from chats.models import *
from rest_framework import serializers


class ChatGroupReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = '__all__'
        depth = 1


class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
