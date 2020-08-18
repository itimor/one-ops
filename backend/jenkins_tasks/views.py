# -*- coding: utf-8 -*-
# author: itimor

from jenkins_tasks.serializers import *
from common.views import ModelViewSet, JsonResponse
from common import status
from collections import OrderedDict
from rest_framework.decorators import action


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    search_fields = ['name']
    filter_fields = ['id', 'name']

    # send
    @action(methods=['post'], url_path='send', detail=False)
    def send(self, request, *args, **kwargs):
        self.watch_audit_log(request)
        data = {'code': 20000, 'msg': 'null'}
        type = request.GET['type']
        if type == 'mail':
            bot_name = request.GET['bot_name']
            bot_obj = MailBot.objects.get(name=bot_name)
            subject = "{}".format(request.form['subject'])
            mail_to = bot_obj.to
            mail_host = bot_obj.host
            mail_user = '{}@{}'.format(bot_obj.user, bot_obj.host)
            mail_pass = bot_obj.pasword
            content = request.data.get('content', 'Hello Pornhub')
            send_mail.delay(subject, mail_to, mail_host, mail_user, mail_pass, content)
        elif type == 'telegram':
            bot_name = request.GET['bot_name']
            content = request.data.get('content', 'Hello Pornhub')
            bot_obj = TelegramBot.objects.get(name=bot_name)
            send_telegram.delay(chat_id=bot_obj.chat_id, text=content)
        else:
            pass

        return JsonResponse(OrderedDict([
            ('results', data)
        ], code=status.HTTP_200_OK))
