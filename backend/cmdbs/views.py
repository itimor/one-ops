# -*- coding: utf-8 -*-
# author: itimor

from cmdbs.serializers import *
from common.views import ModelViewSet, JsonResponse


class HistoryViewSet(ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    search_fields = ['cmd']
    filter_fields = ['num']
