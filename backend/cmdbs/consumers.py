# -*- coding: utf-8 -*-
# author: itimor

import sys
import json
from channels.generic.websocket import WebsocketConsumer
from cmdbs.models import *
import subprocess


class CmdConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close(403)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        save_cmd(text_data_json)
        cmd = subprocess.Popen(text_data_json['cmd'], stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdout=subprocess.PIPE, universal_newlines=True, shell=True, bufsize=1)
        # 实时输出
        while True:
            line = cmd.stdout.readline()
            if line == '' and subprocess.Popen.poll(cmd) == 0:  # 判断子进程是否结束
                break
            sys.stdout.flush()
            if line != '':
                obj = {"text": line.strip()}
                self.send(text_data=json.dumps(obj))


from cmdbs.serializers import *
from rest_framework.renderers import JSONRenderer
from utils.compatibility import text_


def save_cmd(event):
    cmd = event['cmd']
    try:
        obj = History.objects.get(cmd=cmd)
        obj.num += 1
        obj.save()
    except:
        obj = History.objects.create(cmd=cmd, num=1)

    serializer = HistorySerializer(obj)
    j = JSONRenderer().render(serializer.data)
    data = json.loads(text_(j))
    return data
