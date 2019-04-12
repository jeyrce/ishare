# coding: utf-8
"""
Created by Jeeyshe.Ru at 19-3-27 下午2:52, for any more contact me with jeeysie@gmail.com.
Here is the descriptions and some purpose of the file:
    0. 一些工具函数
"""

import datetime
import base64

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

from db import models as _m
from ljx import settings as _st

UserAccount = get_user_model()


def get_value_from_db(key, default):
    # 从extend数据库读取值, 不存在则返回默认值
    obj = _m.Expand.objects.filter(key=key).first()
    return obj.value if obj else default


class ContextUtil(object):
    """
    关于全局模板上下文的工具
    """

    @classmethod
    def origin_art_cnt(cls) -> int:
        # 获取原创文章数量
        return _m.Blog.objects.filter(source__isnull=True, is_active=True).count()

    @classmethod
    def run_days(cls) -> int:
        # 网站运行天数
        start = datetime.datetime.strptime(_st.START, '%Y-%m-%d')
        now = datetime.datetime.now()
        times = now - start
        return times.days

    @classmethod
    def copy_art_cnt(cls) -> int:
        # 获取原创文章数量
        return _m.Blog.objects.filter(source__isnull=False, is_active=True).count()

    @classmethod
    def visit_cnt(cls) -> int:
        # 总访问次数统计
        visit_cnt = int(get_value_from_db('VISIT_CNT', 753))
        return visit_cnt

    @classmethod
    def today_visit_cnt(cls) -> int:
        # 今日访问次数
        today = int(get_value_from_db('TODAY_VISIT_CNT', 0))
        return today

    @classmethod
    def most_read(cls):
        # 阅读次数最多的几条
        num = int(get_value_from_db('MOST_READ_SHOW_NUM', 10))
        query = _m.Blog.objects.order_by('-read').filter(is_active=True)[:num]
        return query

    @classmethod
    def notice(cls):
        # 网站公告
        num = int(get_value_from_db('NOTICE_SHOW_NUM', 3))
        query = _m.Notice.objects.order_by('-add').filter(is_active=True)[:num]
        return query

    @classmethod
    def recommend(cls):
        # 推荐阅读
        num = int(get_value_from_db('RECOMMEND_SHOW_NUM', 10))
        query = _m.Blog.objects.order_by('-add').filter(is_active=True, is_fine=True)[:num]
        return query

    @classmethod
    def random_tags(cls):
        # 随机标签云, 数量在百万以下采用这种方法， 很明显个人博客足够了
        num = int(get_value_from_db('TAG_CLOUD_SHOW_NUM', 20))
        query = _m.Tag.objects.order_by('?').filter(is_active=True)[:num]
        return query

    @classmethod
    def you_may_like(cls, request):
        # 猜你喜欢: 当用户阅读某一文章的详情时，随机取出这篇文章的同类别和同标签文章几篇进行推荐
        raise NotImplementedError()

    @staticmethod
    def cats(pre='A'):
        # 站点除了散文之外的技术博客
        return _m.Category.objects.order_by('-add').filter(is_active=True, pre_cat=pre)


def make_auth_token(obj, salt, join_str='---'):
    # 制作用于标记用户在线的token
    token_string = join_str.join([salt, obj.pk])
    new_string = str(base64.b64encode(bytes(token_string, encoding='utf-8')))
    return new_string.split("'")[1]


def parse_auth_token(token, salt, join_str='---'):
    # 反解token
    obj = object()
    s = base64.b64decode(bytes(token, encoding='utf-8')).decode('utf-8')
    up_salt, up_obj_str = s.split(join_str)
    if not up_salt == salt:
        return obj
    visitor = _m.UserAccount.objects.filter(is_active=True, pk=up_obj_str).first()
    if not visitor:
        return obj
    return visitor


class EmailAuthBackend(ModelBackend):
    """
    使用email作为账户登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username
        try:
            account = UserAccount.objects.get(**{UserAccount.EMAIL_FIELD: email})
        except UserAccount.DoesNotExist:
            pass
        else:
            if account.check_password(password) and self.user_can_authenticate(account):
                return account
