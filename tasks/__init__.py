#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
#=============================================================================
# FileName: __init__.py.py
# Desc: 项目中所需的异步任务
# Author: Jeyrce.Lu
# Email: jeyrce@gmail.com
# HomePage: www.lujianxin.com
# Created: 2019/9/30 下午4:17
#=============================================================================
"""

import celery

app = celery.Celery()

app.config_from_object("tasks.settings")

app.autodiscover_tasks([
    "tasks.mail",
    "tasks.cron",
    "tasks.ops",
])
