# -*- coding: utf-8 -*-
"""
    个人博客, 今日正式奠基,
"""
from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app

__version__ = '0.0.0'
__site__ = 'www.lujianxin.com'
__start__ = '2019-03-08'

__all__ = ('celery_app',)
