# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from common.models import BaseModel


class History(BaseModel):
    cmd = models.TextField(verbose_name='命令')
    num = models.IntegerField(default=0, blank=True, verbose_name='次数')

    class Meta:
        verbose_name = "历史命令"
        verbose_name_plural = verbose_name
