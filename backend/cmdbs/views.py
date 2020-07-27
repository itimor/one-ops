# -*- coding: utf-8 -*-
# author: itimor

from cmdbs.serializers import *
from common.views import ModelViewSet, JsonResponse


class HistoryViewSet(ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    search_fields = ['cmd']
    filter_fields = ['num']


class IdcViewSet(ModelViewSet):
    queryset = Idc.objects.all()
    serializer_class = IdcSerializer
    search_fields = ['name']
    filter_fields = ['name']


class HostGroupViewSet(ModelViewSet):
    queryset = HostGroup.objects.all()
    serializer_class = HostGroupSerializer
    search_fields = ['name']
    filter_fields = ['name']


class HostViewSet(ModelViewSet):
    queryset = Host.objects.all()
    serializer_class = HostSerializer
    search_fields = ['hostname', 'hostname']
    filter_fields = ['hostname', 'hostname']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return HostReadSerializer
        return HostSerializer
