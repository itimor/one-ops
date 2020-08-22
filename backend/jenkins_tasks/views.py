# -*- coding: utf-8 -*-
# author: itimor

from jenkins_tasks.serializers import *
from common.views import ModelViewSet, JsonResponse
from common import status
from collections import OrderedDict
from rest_framework.decorators import action
from core.settings import jj
from django.db.models import Q


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    search_fields = ['name', 'code']
    filter_fields = ['id', 'name', 'code']

    @action(methods=['post'], url_path='stop', detail=False)
    def stop(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        job_name = request.data['code']
        build_id = request.data['build_id']
        job = jj.get_job(job_name)
        job_build = job.get_build(int(build_id))
        s = job_build.stop()
        print(s)
        j = TaskLog.objects.get(code=job_name, build_id=build_id)
        j.status = 4
        j.save()
        data = {'code': 20000, 'build_id': build_id}
        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))

    @action(methods=['post'], url_path='ping', detail=False)
    def ping(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        job_name = 'ping'
        num = request.data['num']
        job = jj.get_job(job_name)
        build_id = job.get_next_build_number()
        params = {"num": num}
        job.invoke(build_params=params)
        TaskLog.objects.create(name='ping测试', code=job_name, build_id=build_id, params=params)
        data = {'code': 20000, 'build_id': build_id}
        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))


class TaskLogViewSet(ModelViewSet):
    queryset = TaskLog.objects.all()
    serializer_class = TaskLogSerializer
    search_fields = ['name', 'code']
    filter_fields = ['build_id', 'name', 'code']

    @action(methods=['get'], url_path='flush', detail=False)
    def flush(self, request, *args, **kwargs):
        tasks = TaskLog.objects.filter(Q(status=1) | Q(status=2))
        for j in tasks:
            job = jj.get_job(j.code)
            try:
                job_build = job.get_build(int(j.build_id))
                j_status = job_build.is_running()
                if j_status is None:
                    j.status = 1
                    j.save()
                    continue
                if j_status:
                    j.status = 2
                    j.save()
                else:
                    if job_build.is_good:
                        j.status = 3
                    else:
                        j.status = 4
                    j.save()
            except:
                j.status = 1
                j.save()

        data = {'code': 20000, 'count': len(tasks)}
        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))
