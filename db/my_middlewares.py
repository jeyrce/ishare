# coding: utf-8
"""
Created by Jeeyshe.Ru at 19-3-27 下午6:04, for any more contact me with jeeyshe@gmail.com.
Here is the descriptions and some purpose of the file:
    0. 自定义中间件
"""

from django.http import QueryDict
from django.core.cache import caches

from db.models import Click, Link, Expand
from ljx.settings import DEFAULT_UA
from db.utils import today_key


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
        # 总访问记录： 暂时直接存库，以后配合celery进行定时任务存库
        obj, is_created = Expand.objects.get_or_create(key='VISIT_CNT', defaults={'key': 'VISIT_CNT', 'value': '1'})
        if request.META.get('PATH_INFO', '-').startswith('/x/'):
            if not is_created:
                obj.value = str(int(obj.value) + 1)
                obj.save(update_fields=('value',))
            # 今日访问记录: 使用redis进行高速缓存
            cache = caches['four']
            cnt = cache.get(today_key(), 0)
            new = cnt + 1 if cnt else 1
            cache.set(today_key(), new, 60 * 60 * 24)


class LinkClickMiddleware(BaseCustomMiddleware):
    """
    广告, 友情链接点击记录中间件
    """

    def after_make_response(self, request):
        # 记录ip, ua关键信息
        if request.META.get('PATH_INFO', '') == '/x/goto/':
            LK = request.GET.get('uri', '/')
            link_obj = Link.objects.filter(link=LK).only(*('id',)).first()
            if link_obj:
                UA = request.META.get('HTTP_USER_AGENT', DEFAULT_UA)
                IP = request.META.get('REMOTE_ADDR', '0.0.0.0')
                try:
                    Click.objects.create(link_id=link_obj.id, ip=IP, user_agent=UA)
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
