# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url
from rest_framework import routers
from jenkins_tasks.views import TaskViewSet

router = routers.DefaultRouter()

router.register(r'task', TaskViewSet)

urlpatterns = [
]

urlpatterns += router.urls
