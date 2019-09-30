#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
#=============================================================================
# FileName: __init__.py.py
# Desc: 项目中所需的异步任务
# Author: jeeyshe
# Email: jianxin.lu@woqutech.com
# HomePage: www.lujianxin.com
# Version: 7.0.0
# Created: 2019/9/30 下午4:17
#=============================================================================
"""

import celery

app = celery.Celery()

app.config_from_object("tasks.settings")
