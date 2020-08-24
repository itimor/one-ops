# -*- coding: utf-8 -*-
# author: itimor

import os

APP_ENV = 'test'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '64318ob@vbou7h50)b0a_pfda4d$bw2nhl4h*m$qo0_e_fxw=658!z*x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ops',
        'USER': 'root',
        'PASSWORD': 'momo520',
        'HOST': 'localhost',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks=0;",
        }
    }
}
# 加载 mysql
import pymysql

pymysql.install_as_MySQLdb()

REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%Y-%m-%d %H:%M:%S",
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.StandardResultsSetPagination',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['../frontend/dist'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ASGI_APPLICATION = "core.routing.application"  # 上面新建的 asgi 应用
CHANNEL_LAYERS = {
    'default': {
        # 这里用到了 channels_redis
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379)],  # 配置你自己的 redis 服务信息
        },
    }
}

# 长时间并耗时，后期需要查看日志的任务放jenkins
from jenkinsapi.jenkins import Jenkins

jenkins_info = {
    'baseurl': 'http://jenkins.xxoo.com',
    'username': 'admin',
    'password': '11871bd159bd19da9ab624d161c569e3c8'
}
try:
    jj = Jenkins(baseurl=jenkins_info['baseurl'], username=jenkins_info['username'], password=jenkins_info['password'])
except:
    jj = None
    print('jenkins连接不可用')
