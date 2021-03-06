# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from common.models import BaseModel


class History(BaseModel):
    cmd = models.TextField(verbose_name='命令')
    num = models.IntegerField(default=1, blank=True, verbose_name='次数')

    class Meta:
        verbose_name = "历史命令"
        verbose_name_plural = verbose_name


class Idc(BaseModel):
    name = models.CharField(max_length=32, unique=True, verbose_name="名称")
    code = models.CharField(max_length=32, unique=True, verbose_name='代码')
    country = models.CharField(max_length=32, null=True, blank=True, verbose_name="国家")
    area = models.CharField(max_length=32, null=True, blank=True, verbose_name="区域")
    addr = models.CharField(max_length=32, null=True, blank=True, verbose_name="详细地址地址")
    user = models.CharField(max_length=30, null=True, blank=True, verbose_name="负责人")
    tel = models.CharField(max_length=32, null=True, blank=True, verbose_name="联系电话")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'idc'
        verbose_name_plural = verbose_name


class HostGroup(BaseModel):
    name = models.CharField(max_length=32, unique=True, verbose_name='主机组')
    code = models.CharField(max_length=32, unique=True, verbose_name='代码')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '主机组'
        verbose_name_plural = verbose_name


ASSET_STATUS = {
    0: '待初始化',
    1: '已使用',
    2: '未使用',
    3: '待下线',
    4: '已下线',
}

ASSET_TYPE = {
    1: "物理机",
    2: "虚拟机",
    3: "容器",
    4: "网络设备",
    5: "其他设备"
}

OS_TYPE = {
    1: "centos",
    2: "windows",
    3: "debian",
    4: "other",
}


class Host(BaseModel):
    hostname = models.CharField(max_length=50, unique=True, verbose_name="主机名")
    ip = models.CharField(max_length=100, unique=True, verbose_name="主IP")
    other_ip = models.CharField(max_length=100, null=True, blank=True, verbose_name="其他IP")
    have_net = models.BooleanField(default=False, verbose_name="有外网")
    netmask = models.CharField(max_length=20, null=True, blank=True, verbose_name="子网掩码")
    gateway = models.CharField(max_length=20, null=True, blank=True, verbose_name="网关")
    dns = models.CharField(max_length=20, null=True, blank=True, verbose_name="dns")
    vcenter = models.CharField(max_length=20, null=True, blank=True, verbose_name="所在vcenter地址")
    os = models.CharField(choices=tuple(OS_TYPE.items()), default=1, max_length=30, verbose_name="操作系统")
    cpu = models.CharField(max_length=100, null=True, blank=True, verbose_name="CPU信息")
    cpu_num = models.SmallIntegerField(null=True, blank=True, verbose_name="cpu个数")
    memory = models.SmallIntegerField(default='1', null=True, blank=True, verbose_name="内存信息")
    sys_disk = models.CharField(max_length=100, null=True, blank=True, verbose_name="系统磁盘")
    data_disk = models.CharField(max_length=100, null=True, blank=True, verbose_name="数据磁盘")
    other_disk = models.CharField(max_length=100, null=True, blank=True, verbose_name="其他磁盘")
    datastore = models.CharField(max_length=100, null=True, blank=True, verbose_name="数据中心名称")
    groups = models.ManyToManyField(HostGroup, blank=True, related_name='host_group', verbose_name='主机组')
    idc = models.ForeignKey(Idc, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="机房")
    asset_type = models.CharField(choices=tuple(ASSET_TYPE.items()), default=2, max_length=30, verbose_name="设备类型")
    status = models.CharField(choices=tuple(ASSET_STATUS.items()), default=0, max_length=30, verbose_name="设备状态")
    an = models.CharField(max_length=20, null=True, blank=True, verbose_name="资产编号")
    sn = models.CharField(max_length=20, null=True, blank=True, verbose_name="机器码")

    def __str__(self):
        return self.hostname

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = verbose_name
