#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 邮件异步任务
"""
from smtplib import SMTP_SSL

import celery
from ljx.settings import (EMAIL_HOST, EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_PORT, EMAIL_USE_SSL, EMAIL_USE_TLS,
                          EMAIL_SUBJECT_PREFIX)


@celery.task(name="tasks.mail.send_message")
def send_message():
    print("=====>send___777")
