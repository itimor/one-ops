# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url
from rest_framework import routers
from cmdbs.views import HistoryViewSet, IdcViewSet, HostGroupViewSet, HostViewSet, inithost

router = routers.DefaultRouter()

router.register(r'history', HistoryViewSet)
router.register(r'idc', IdcViewSet)
router.register(r'hostgroup', HostGroupViewSet)
router.register(r'host', HostViewSet)

urlpatterns = [
    url(r'^inithost/', inithost.as_view()),
]

urlpatterns += router.urls
