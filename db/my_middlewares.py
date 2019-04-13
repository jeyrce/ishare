# coding: utf-8
"""
Created by Jeeyshe.Ru at 19-3-27 下午6:04, for any more contact me with jeeyshe@gmail.com.
Here is the descriptions and some purpose of the file:
    0. 自定义中间件
"""

from django.http import QueryDict

from db.models import Click, Link
from ljx.settings import DEFAULT_UA


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
    访客访问记录中间件， 统计今日访问次数和历史总访问次数
    """

    def after_make_response(self, request):
        # 今日访问次数的临时数据由定时任务每晚0点执行
        # TODO： 更新今日访问次数
        # TODO： 更新历史访问次数
        pass


class LinkClickMiddleware(BaseCustomMiddleware):
    """
    广告, 友情链接点击记录中间件
    """

    def after_make_response(self, request):
        # 记录ip, ua关键信息
        if request.META.get('PATH_INFO', '') == '/x/goto/':
            LK = request.GET.get('uri', '/')
            if Link.objects.filter(link=LK).count():
                UA = request.META.get('HTTP_USER_AGENT', DEFAULT_UA)
                IP = request.META.get('REMOTE_ADDR')
                try:
                    Click.objects.create(link_id=LK, ip=IP, user_agent=UA)
                except:
                    pass


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
