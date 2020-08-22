# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from common.models import BaseModel


# name 创建主机， 主机释放
class Task(BaseModel):
    name = models.CharField(max_length=64, unique=True, verbose_name='名称')
    code = models.CharField(max_length=64, unique=True, verbose_name='code')
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "jenkins任务"
        verbose_name_plural = verbose_name


# 1.等待 2.正在运行 3.成功 4.取消 5.失败
STATUS_TYPE = {
    1: "PENDING",
    2: "RUNNING",
    3: "SUCCESS",
    4: "ABORTED",
    5: "FAILURE",
}


class TaskLog(BaseModel):
    name = models.CharField(max_length=64, verbose_name='名称')
    code = models.CharField(max_length=64, verbose_name='code')
    build_id = models.CharField(max_length=64, unique=True, verbose_name='构建id')
    params = models.TextField(null=True, blank=True, verbose_name='一推参数')
    status = models.CharField(choices=tuple(STATUS_TYPE.items()), default=2, max_length=1, verbose_name="状态")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = "任务日志"
        verbose_name_plural = verbose_name
