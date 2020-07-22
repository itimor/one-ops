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
    messages = ChatMessageReadSerializer(many=True, read_only=True)

    class Meta:
        model = ChatGroup
        fields = '__all__'
        depth = 1


class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = '__all__'

    def create(self, validated_data):
        join_user = validated_data.pop('join_user')
        obj = ChatGroup.objects.create(**validated_data)
        obj.join_user.set(join_user)
        obj.save()
        ChatMessage.objects.create(group=obj, create_user=obj.create_user, message="快上车，来不解释了！")
        return obj
