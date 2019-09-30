#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 邮件异步任务
"""

import time
import celery


@celery.task(name="tasks.mail.send_message")
def send_message():
    time.sleep(7)
    print("=====>send___777")
