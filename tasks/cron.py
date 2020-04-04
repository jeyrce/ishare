# coding: utf-8
"""
Created by Jeeyshe 2020/4/4 下午5:16, contact with jeeyshe@gmail.com or website https://www.lujianxin.com
---------------------------------------------------------------------------------------------------------
>>> 项目中的一些定时任务
"""

from django.core.mail import send_mail, send_mass_mail

from tasks import app
from ishare.settings import EMAIL_SUBJECT_PREFIX
from blog.models import Expand, Blog, Link


@app.task(name='cron.update_visit_count')
def update_visit_count(*args, **kwargs):
    print("更新网站浏览量")


@app.task(name='cron.update_like_click')
def update_like_click(*args, **kwargs):
    print("更新文章点赞量")


@app.task(name='cron.notify_new_link')
def notify_new_link(*args, **kwargs):
    # send_mass_mail()
    print("今日新增的待通过友链")


@app.task(name='cron.notify_new_article')
def notify_new_article(*args, **kwargs):
    # send_mail()
    print("今日新增待审核文章")
