# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url
from rest_framework import routers
from cmdbs.views import HistoryViewSet

router = routers.DefaultRouter()

router.register(r'history', HistoryViewSet)

urlpatterns = [
]

urlpatterns += router.urls
