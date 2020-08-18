# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from common.models import BaseModel


# name 初始化主机， 主机释放
class Task(BaseModel):
    name = models.CharField(max_length=64, unique=True, verbose_name='名称')
    code = models.CharField(max_length=64, unique=True, verbose_name='code')
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "jenkins任务"
        verbose_name_plural = verbose_name


STATUS_TYPE = {
    1: "running",
    2: "success",
    3: "error",
}


class TaskLog(BaseModel):
    name = models.CharField(max_length=64, unique=True, verbose_name='名称')
    code = models.CharField(max_length=64, unique=True, verbose_name='code')
    build_id = models.CharField(max_length=64, unique=True, verbose_name='构建id')
    params = models.TextField(null=True, blank=True, verbose_name='一推参数')
    status = models.CharField(choices=tuple(STATUS_TYPE.items()), default=2, max_length=1, verbose_name="状态")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "任务日志"
        verbose_name_plural = verbose_name
