# -*- coding: utf-8 -*-
# author: itimor

import sys
import json
from channels.generic.websocket import WebsocketConsumer
from cmdbs.cmdrun import run_shell
from cmdbs.serializers import *
from rest_framework.renderers import JSONRenderer
from utils.compatibility import text_
from celery_tasks.tasks import tailf


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


class CmdConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close(403)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        save_cmd(text_data_json)
        a = run_shell(text_data_json['cmd'])
        # 实时输出
        while True:
            line = a.stdout.readline()
            # print(line, end='')
            if line == '' or a.poll() is not None:  # 判断子进程是否结束
                break
            sys.stdout.flush()
            if line != '':
                obj = {"text": line.strip()}
                self.send(text_data=json.dumps(obj))


class TailfConsumer(WebsocketConsumer):
    def connect(self):
        self.filename = self.scope["url_route"]["kwargs"]["filename"]
        self.result = tailf.delay(self.filename, self.channel_name)
        print('connect:', self.channel_name, self.result.id)
        self.accept()

    def disconnect(self, close_code):
        # 中止执行中的Task
        self.result.revoke(terminate=True)
        print('disconnect:', self.filename, self.channel_name)
        self.close()

    def send_log(self, event):
        self.send(text_data=json.dumps({
            "message": event["message"]
        }))
