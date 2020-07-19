# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from systems.models import User
from common.models import BaseModel


class ChatGroup(BaseModel):
    name = models.CharField(max_length=32, unique=True, verbose_name='名称')
    code = models.CharField(max_length=32, unique=True, verbose_name='代码')
    create_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="create_user", verbose_name='创建者')
    join_user = models.ManyToManyField(User, related_name="join_user", verbose_name='群员')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '群组'
        verbose_name_plural = verbose_name


class ChatMessage(BaseModel):
    create_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='创建者')
    group = models.ForeignKey(ChatGroup, on_delete=models.CASCADE, verbose_name='群组')
    message = models.TextField('消息内容')

    class Meta:
        verbose_name = '消息'
        verbose_name_plural = verbose_name
