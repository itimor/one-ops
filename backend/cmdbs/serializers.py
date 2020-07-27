# -*- coding: utf-8 -*-
# author: itimor

from cmdbs.models import *
from rest_framework import serializers


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'


class IdcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idc
        fields = '__all__'


class HostGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostGroup
        fields = '__all__'


class HostReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'
        depth = 1


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'
