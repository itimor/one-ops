# -*- coding: utf-8 -*-
# author: itimor


from django.conf.urls import url
from rest_framework import routers

router = routers.DefaultRouter()

# router.register(r'notice', NoticeViewSet)

urlpatterns = [
]

urlpatterns += router.urls
