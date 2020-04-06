#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Celery 配置

import os
import datetime

from kombu import Exchange, Queue
import django
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ishare.settings")
django.setup()

# 记录日志
CELERYD_HIJACK_ROOT_LOGGER = True
CELERY_TIMEZONE = 'Asia/Shanghai'

# 注册Celery任务, 或者使用celery.autodiscover_tasks也可
# CELERY_IMPORTS = (
#     "tasks.mail",
# )

# 序列化方法
CELERY_TASK_SERIALIZER = "pickle"
# 指定任务接受的序列化类型.
CELERY_ACCEPT_CONTENT = ["msgpack", "pickle", "json", "yaml", ]
# 结果序列化方法
CELERY_RESULT_SERIALIZER = "pickle"
# 结果保存
CELERY_RESULT_BACKEND = 'redis://:{}@{}:{}/2'.format("lujianxin.com", "127.0.0.1", 6379)
# Broker使用redis
BROKER_URL = 'redis://:{}@{}:{}/3'.format("lujianxin.com", "127.0.0.1", 6379)

default_exchange = Exchange('default', type='direct')
topic_exchange = Exchange('topic', type='topic')
fanout_exchange = Exchange('fanout', type='fanout')

CELERY_QUEUES = (
    Queue('default', default_exchange, routing_key='default'),
    Queue('topic', topic_exchange, routing_key='topic'),
    Queue('fanout', fanout_exchange, routing_key='fanout'),
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'

# 定时任务配置如下
CELERYBEAT_SCHEDULE = {
    # 更新网站访问量
    'loop_task_1': {
        'task': 'cron.update_visit_count',
        'schedule': datetime.timedelta(hours=1),  # 周期任务: 每隔time执行一次
        'args': (),
    },
    # 刷新文章点赞到库中
    'loop_task_2': {
        'task': 'cron.update_like_click',
        'schedule': datetime.timedelta(hours=1),
        'args': (),
    },
    # 提醒站长新的友链申请
    'fixed_task_3': {
        'task': 'cron.notify_new_link',
        'schedule': crontab(hour='21', minute='00'),  # 定时任务: 固定的时间点执行
        'args': (),
    },
    # 提醒站长新增的待审核文章
    'fixed_task_4': {
        'task': 'cron.notify_new_article',
        'schedule': crontab(hour='21', minute='30'),
        'args': (),
    },
    # 每月向友链推荐阅读
    'fixed_task_5': {
        'task': 'cron.recommend_month',
        'schedule': crontab(day_of_month='1', hour='10', minute='30'),
        'args': (),
    },
}
