# coding: utf-8
"""
Created by Jeeyshe.Ru at 2019/4/10 下午7:57, for any more contact me with jeeyshe@gmail.com.
Here is the descriptions and some purpose of the file:
    0. 初始化celery
"""

from __future__ import absolute_import, unicode_literals
import os

from ljx.settings import MAIN_APPS
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ljx.settings')

app = Celery('ljx')

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(MAIN_APPS)
