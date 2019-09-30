#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Celery 配置


from kombu import Exchange, Queue

# 记录日志
CELERYD_HIJACK_ROOT_LOGGER = False

# 注册Celery任务
CELERY_IMPORTS = (
    "tasks.mail",
)

# 序列化方法
CELERY_TASK_SERIALIZER = "json"
# 结果保存
CELERY_RESULT_BACKEND = 'redis://:{}@{}:{}/2'.format("ljX.07", "127.0.0.1", 6379)
# Broker使用redis
BROKER_URL = 'redis://:{}@{}:{}/3'.format("ljX.07", "127.0.0.1", 6379)

default_exchange = Exchange('default', type='direct')
topic_exchange = Exchange('topic', type='topic')
fanout_exchange = Exchange('fanout', type='fanout')

CELERY_QUEUES = (
    Queue('default', default_exchange, routing_key='default'),
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_DEFAULT_EXCHANGE = 'default'
CELERY_DEFAULT_ROUTING_KEY = 'default'
