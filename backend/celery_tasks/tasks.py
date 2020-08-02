# -*- coding: utf-8 -*-
# author: itimor

from celery import shared_task
from time import sleep
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from utils.init_host import gogobar


@shared_task
def add(x, y):
    sleep(30)
    return x + y


@shared_task
def send_mail(subject, mail_to, mail_host, mail_user, mail_password, content):
    import smtplib
    from email.mime.text import MIMEText
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = subject
    message['From'] = mail_user
    message['To'] = mail_to[0:]
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host)
        smtpObj.login(mail_user, mail_password)
        smtpObj.sendmail(mail_user, mail_to, message.as_string())
        smtpObj.quit()
    except smtplib.SMTPException as e:
        print(e)


@shared_task
def send_telegram(token, chat_id, content):
    import telegram
    bot = telegram.Bot(token=token)
    bot.send_message(chat_id=chat_id, text=content)


@shared_task
def init_host(log_path, log_name, hosts, monitor_node):
    for host in hosts:
        hostname = host['hostname']
        ip = host['ip']
        gogobar(log_path, log_name, hostname, ip, monitor_node)


@shared_task
def tailf(filename, channel_name):
    channel_layer = get_channel_layer()
    # while True:
    #     sleep(1)
    #     async_to_sync(channel_layer.send)(
    #         channel_name,
    #         {
    #             "type": "send_log",
    #             "message": "微信公众号【运维咖啡吧】原创 版权所有 " + str(1)
    #         }
    #     )
    try:
        with open(filename) as f:
            f.seek(0, 2)
            while True:
                line = f.readline()
                if line:
                    async_to_sync(channel_layer.send)(
                        channel_name,
                        {
                            "type": "send_log",
                            "message": line
                        }
                    )
                else:
                    sleep(0.5)
    except Exception as e:
        print(e)
