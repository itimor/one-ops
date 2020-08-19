# -*- coding: utf-8 -*-
# author: itimor

import json
from channels.generic.websocket import WebsocketConsumer
from cmdbs.serializers import *
from core.settings import jj


class JenkingLogConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        self.close(403)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        build_name = text_data_json['code']
        build_id = int(text_data_json['build_id'])
        # 实时输出
        a = jj.get_job(build_name).get_build(build_id)
        status = a.is_running()
        logs = a.stream_logs()
        if status:
            for line in logs:
                obj = {"text": line.strip()}
                self.send(text_data=json.dumps(obj))
        else:
            for line in logs:
                for i in line.splitlines():
                    obj = {"text": i}
                    self.send(text_data=json.dumps(obj))
