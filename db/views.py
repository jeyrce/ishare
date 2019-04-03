# coding: utf-8
"""
Created by Jeeyshe.Ru at 19-3-27 下午7:22, for any more contact me with jeeyshe@gmail.com.
Here is the descriptions and some purpose of the file:
    0. 博客主要业务逻辑视图
"""

from django.http.response import JsonResponse, HttpResponse, Http404
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, resolve_url, redirect

from ljx.views import OpenView, RestfulView
from db import models as m
from db.utils import ContextUtil
from db.forms import CommentForm


class DoingView(OpenView):
    """
    先占个坑
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'doing.html')


class ArticleObj(RestfulView):
    # 前台和文章有关的逻辑

    model = m.Blog

    def get_obj(self, pk):
        return self.model.objects.filter(pk=pk, is_active=True).first()

    def get_cnxh(self, obj):
        # 获取同类型文章猜你喜欢
        queryset = self.model.objects.filter(is_active=True, cat_id=obj.cat.id).order_by('?')[:10]
        return queryset

    def get_others(self, obj):
        # 作者其他文章
        return self.model.objects.filter(is_active=True, author_id=obj.author_id).order_by('-add')[:10]

    def get_next(self, obj):
        # 获取下一篇： 按发表时间
        return self.model.objects.filter(is_active=True, add__gt=obj.add).order_by('-add').first()

    def get_prev(self, obj):
        # 获取上一篇： 按发表时间
        return self.model.objects.filter(is_active=True, add__lt=obj.add).order_by('-add').first()

    def get(self, request, pk):
        # 获取文章详情
        obj = self.get_obj(pk)
        if not obj:
            raise Http404()

        ctx = {
            'art': obj,
            'tags': ContextUtil.random_tags(),
            'cnxh': self.get_cnxh(obj),
            'others': self.get_others(obj),
            'next': self.get_next(obj),
            'prev': self.get_prev(obj),
            'cform': CommentForm()
        }

        return render(request, 'detail.html', ctx)

    def post(self, request, pk):
        obj = self.get_obj(pk)
        # 文章点赞
        raise NotImplementedError()

    def patch(self, request, pk):
        # 修改文章
        print(self.request.PATCH)
        return JsonResponse({"code": 0, "msg": 'put xxx'})

    def delete(self, request, pk):
        # 删除文章
        raise NotImplementedError()


class ArticleAdd(RestfulView):

    def get(self, request):
        # 发表新的文章
        raise NotImplementedError()


class CommentAdd(View):
    """
    添加评论楼层
    """

    def post(self, request):
        print(self.request.POST)
        return HttpResponse('ok')


class Soul(OpenView):
    # 获取文学创作类列表
    def get(self, request, *args, **kwargs):
        ctx = {
            'soul_list': self.get_art_list(),
            'tags': ContextUtil.random_tags(),
            'page': {
                'title': '文学作品 | 陆鉴鑫的博客',
                'keywords': '文艺青年、个人博客、原创文章、内容创作、文学创作、文学梦想',
                'description': '陆鉴鑫的博客，一个助力实现文学梦想，技术干货创作和分享的开放平台。',
            }
        }
        return render(request, 'soul.html', ctx)

    def get_art_list(self):
        # 获取列表
        query = m.Blog.objects.filter(is_active=True, cat_id=1)
        return query


class Link(RestfulView):
    """
    友链相关
    """

    def get(self, request, *args, **kwargs):
        ctx = {
            'public_links': self.get_public_links(),
            'public_cnt': self.public_cnt,
            'person_cnt': self.person_cnt,
            'biz_cnt': self.biz_cnt,
            'person_links': self.get_person_links(),
            'biz_links': self.get_biz_links(),
            'page': {
                'title': '友情链接 | 陆鉴鑫的博客',
                'keywords': '友情链接、公益链接、个人主页、商业广告',
                'description': '陆鉴鑫的博客，一个助力实现文学梦想，技术干货创作和分享的开放平台。',
            },
            'declare': '友链说明',
            'desc': '本站接受个人博客链接、真实可信的广告链接作为友链，请自行提交或联系站长后台添加，自行提交的链接通过审核方可显示，请耐心等待。',
        }
        return render(request, 'link.html', ctx)

    def get_person_links(self):
        # 获取链接
        return m.Link.objects.filter(is_active=True, cat=1)

    @property
    def person_cnt(self):
        return self.get_person_links().count()

    def get_public_links(self):
        # 公益链接
        return m.Link.objects.filter(is_active=True, cat=0)

    @property
    def public_cnt(self):
        return self.get_public_links().count()

    def get_biz_links(self):
        # 商业广告
        return m.Link.objects.filter(is_active=True, cat=2)

    @property
    def biz_cnt(self):
        return self.get_biz_links().count()


class Message(RestfulView):
    """
    留言板
    """
    def get(self, request, *args, **kwargs):
        ctx = {

        }
        return render(request, 'msg.html', ctx)
