# coding: utf-8
"""
Created by Jeyrce 2020/5/1 上午10:29, contact with jeyrce@gmail.com or website https://www.lujianxin.com
---------------------------------------------------------------------------------------------------------
>>> 一些异步任务
"""

import logging

from django.db.models.query import F

from blog.models import Blog
from tasks import app

logger = logging.getLogger(__name__)


@app.task(name="ops.update_art_like")
def update_art_like(pk):
    """
    更新文章点赞量
    """
    Blog.objects.filter(pk=pk).update(like=F("like") + 1)
    logger.info("更新文章点赞量成功: {}".format(pk))
