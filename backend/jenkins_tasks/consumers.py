# -*- coding: utf-8 -*-
# author: itimor

import json
from channels.generic.websocket import WebsocketConsumer
from cmdbs.serializers import *
from core.settings import jj


class JenkingLogConsumer(WebsocketConsumer):
    def connect(self):
        self.build_name = self.scope["url_route"]["kwargs"]["build_name"]
        self.build_id = int(self.scope["url_route"]["kwargs"]["build_id"])
        self.accept()

    def disconnect(self, close_code):
        self.close(403)

    def receive(self, text_data):
        # 实时输出
        a = jj.get_job(self.build_name).get_build(self.build_id)
        print(a)
        for line in a.stream_logs():
            obj = {"text": line.strip()}
            self.send(text_data=json.dumps(obj))
