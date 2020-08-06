# -*- coding: utf-8 -*-
# author: itimor

from cmdbs.serializers import *
from common.views import ModelViewSet, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.index import gen_time_pid
from celery_tasks.tasks import init_host
from utils.init_host import gogobar


class HistoryViewSet(ModelViewSet):
    queryset = History.objects.all().order_by('-num')
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
    search_fields = ['hostname', 'ip']
    filter_fields = ['hostname', 'status', 'groups', 'idc']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve'] or self.resultData:
            return HostReadSerializer
        return HostSerializer


class inithost(APIView):
    """初始化主机"""

    def post(self, request, *args, **kwargs):
        ret = {'code': 20000, 'msg': "success"}
        log_path = '/tmp/cmdb_log'
        log_name = gen_time_pid('inithost')
        hosts = request.data["hosts"]
        monitor_node = "aa"
        init_host.delay(log_path, log_name, hosts, monitor_node)
        ret['results'] = {"log_path": log_path, "log_name": log_name}
        return Response(ret)
