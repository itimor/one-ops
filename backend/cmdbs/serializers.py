# -*- coding: utf-8 -*-
# author: itimor

from cmdbs.models import *
from rest_framework import serializers


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = '__all__'
