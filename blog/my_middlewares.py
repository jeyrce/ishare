# coding: utf-8
"""
Created by Jeeyshe.Ru at 19-3-27 下午6:04, for any more contact me with jeyrce@gmail.com.
Here is the descriptions and some purpose of the file:
    0. 自定义中间件
"""

from django.http import QueryDict
from django.core.cache import caches

from blog.utils import today_key


class BaseCustomMiddleware(object):
    """
    中间件模板，自定义的中间件继承于此类
    如果需要在处理请求之前做什么事， 需要是实现before_make_response(request)方法
    之后，则实现after_make_response(request)方法
    注意：
        0. 可以实现其中一种方法， 也可两种都不实现
    """

    def __init__(self, get_response):
        # 暂存请求对象
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(self, 'before_make_response'):
            request = self.before_make_response(request)
        response = self.get_response(request)
        if hasattr(self, 'after_make_response'):
            self.after_make_response(request)
        return response


class VisitCountMiddleware(BaseCustomMiddleware):
    """
    访客访问记录中间件， 统计历史总访问次数
    """

    def after_make_response(self, request):
        if request.META.get('PATH_INFO', '-').startswith('/x/'):
            cache = caches['four']
            # 总访问记录: 临时存储在redis, 由celery每小时同步到mysql库中
            total_cnt = cache.get('total', 0)
            cache.set('total', total_cnt + 1, 60 * 60 + 60)  # 此处设定时间只要大于1h即可, 同步时会重置时间
            # 今日访问记录: 使用redis进行高速缓存
            today_cnt = cache.get(today_key(), 0)
            cache.set(today_key(), today_cnt + 1, 60 * 60 * 24 + 60)


class AllMethodSupportMiddleware(BaseCustomMiddleware):
    """
    用于支持put, patch, delete请求方式
    """

    extend_methods = ['PUT', 'PATCH', 'DELETE']

    def before_make_response(self, request):
        # 将需要的参数信息封装一下
        if request.method.upper() in self.extend_methods:
            setattr(request, request.method.upper(), QueryDict(request.body))
        return request
