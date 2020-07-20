# -*- coding: utf-8 -*-
# author: itimor

from chats.models import *
from rest_framework import serializers


class ChatMessageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'
        depth = 1


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'


class ChatGroupReadSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatGroup
        fields = '__all__'
        depth = 1


class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = '__all__'
