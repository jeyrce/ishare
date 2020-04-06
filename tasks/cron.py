# coding: utf-8
"""
Created by Jeeyshe 2020/4/4 下午5:16, contact with jeeyshe@gmail.com or website https://www.lujianxin.com
---------------------------------------------------------------------------------------------------------
>>> 项目中的一些定时任务
"""
import logging
import datetime
import time

from django.core.mail import send_mail
from django.core.cache import caches
from django.contrib.auth import get_user_model
from django.template import loader

from tasks import app
from blog.models import Expand, Blog, Link
from tasks.mail import add_prefix, supervisor_receivers, webmaster_receivers
from ishare.settings import SERVER_EMAIL

logger = logging.getLogger(__name__)
UserAccount = get_user_model()


@app.task(name='cron.update_visit_count')
def update_visit_count(*args, **kwargs):
    """
    每小时从redis更新网站总浏览量到mysql
    """
    logger.info("Start update visit count")
    cache = caches['four']
    obj, is_created = Expand.objects.get_or_create(key='VISIT_CNT', defaults={'key': 'VISIT_CNT', 'value': '1'})
    if not is_created:
        real = cache.get('total', 0)
        obj.value = str(int(obj.value) + real)
        obj.save(update_fields=('value',))
        cache.set('total', 0, 60 * 60 + 60)
    logger.info("更新网站浏览量完成")


@app.task(name='cron.update_like_click')
def update_like_click(*args, **kwargs):
    """
    每小时将文章点赞量更新到mysql
    """
    logger.info('Start update blog like')
    cache = caches['four']
    query = Blog.objects.filter(is_active=True)

    def update_blog_like(blog):
        key = "like_{}".format(blog.pk)
        blog.like += cache.get(key, 0)
        blog.save(update_fields=('like',))
        cache.set(key, 0, 60 * 60)

    map(update_blog_like, query)
    logger.info("更新文章点赞量完成")


@app.task(name='cron.notify_new_link')
def notify_new_link(*args, **kwargs):
    """
    每天定时提醒今日新增友链
    """
    logger.info("Start notify new link today")
    now = datetime.datetime.now()
    start = now - datetime.timedelta(days=1, minutes=3)
    links = Link.objects.filter(is_active=False, add__gte=start, add__lt=now)
    total = links.count()
    logger.info("Find %s new links" % total)
    if total > 0:
        html_email = loader.render_to_string(
            'mail/new_link_today.html',
            context={
                'title': 'New Link Today',
                'total': total,
                'public': links.filter(cat=0),
                'personal': links.filter(cat=1),
                'business': links.filter(cat=2),
            }
        )
        send_mail(
            subject=add_prefix("新增友链通知"),
            message='',
            from_email=SERVER_EMAIL,
            recipient_list=supervisor_receivers(),
            html_message=html_email,
        )
    logger.info("今日新增的待通过友链")


@app.task(name='cron.notify_new_article')
def notify_new_article(*args, **kwargs):
    """
    每天定时提醒今日新增待审核文章
    """
    logger.info("Start notify new article today")
    now = datetime.datetime.now()
    start = now - datetime.timedelta(days=1, minutes=3)
    blogs = Blog.objects.filter(is_active=False, add__lt=now, add__gte=start)
    total = blogs.count()
    logger.info("Find %s new blog" % total)
    if total > 0:
        html_email = loader.render_to_string(
            'mail/new_blog_today.html',
            context={
                'title': 'New Blog Today',
                'total': total,
                'blogs': blogs,
            }
        )
        send_mail(
            subject=add_prefix("新增文章通知"),
            message="",
            from_email=SERVER_EMAIL,
            recipient_list=supervisor_receivers(),
            html_message=html_email,
        )
    print("今日新增待审核文章")


@app.task(name='cron.recommend_month')
def recommend_month(*args, **kwargs):
    """
    每月向友链发送阅读推荐
    """
    logger.info("Start recommend to friend-links")
    now = datetime.datetime.now()
    start = now - datetime.timedelta(days=30, hours=1)
    blogs = Blog.objects.filter(is_active=False, add__lt=now, add__gte=start)
    total = blogs.count()
    logger.info("Find %s new blog" % total)
    links = Link.objects.filter(is_active=True)
    if total > 0:
        for link in links:
            html_email = loader.render_to_string(
                'mail/new_blog_this_month.html',
                context={
                    'title': 'New Blog This Month',
                    'total': total,
                    'link': link,
                    'blogs': blogs,
                    'days': datetime.timedelta(now - link.add).days,
                }
            )
            try:
                send_mail(
                    subject=add_prefix("友链推荐阅读通知"),
                    message="",
                    from_email=SERVER_EMAIL,
                    recipient_list=[link.email],
                    html_message=html_email,
                )
            except Exception as e:
                logger.error("通知{}站长失败: {}".format(link.link_name, e))
            time.sleep(5)
    print("每月总结完毕")
