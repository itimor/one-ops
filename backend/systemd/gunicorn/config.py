# -*- coding: utf-8 -*-
# author: itimor

import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

bind = "0.0.0.0:1688"  # 绑定的ip与端口
backlog = 512  # 监听队列数量，64-2048
chdir = '/data/projects/one-ops/backend'  # gunicorn要切换到的目的工作目录
worker_class = 'sync'  # 使用 gevent 模式，还可以使用 sync 模式，默认的是sync模式
workers = 6  # multiprocessing.cpu_count()    #进程数
threads = 8  # multiprocessing.cpu_count()*4 #指定每个进程开启的线程数
loglevel = 'info'  # 日志级别，这个日志级别指的是错误日志的级别，而访问日志的级别无法设置
access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'

accesslog = "/data/logs/oms/gunicorn_access.log"  # 访问日志文件
errorlog = "/data/logs/oms/gunicorn_error.log"  # 错误日志文件
# accesslog = "-"  # 访问日志文件，"-" 表示标准输出
# errorlog = "-"  # 错误日志文件，"-" 表示标准输出

proc_name = 'fuck'  # 进程名
