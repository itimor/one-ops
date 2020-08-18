# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from common.models import BaseModel


class Task(BaseModel):
    name = models.CharField(max_length=64, unique=True, verbose_name='名称')
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "jenkins任务"
        verbose_name_plural = verbose_name

