# coding: utf-8
"""
Created by Jeeyshe.Ru at 19-3-27 下午7:22, for any more contact me with jeeyshe@gmail.com.
Here is the descriptions and some purpose of the file:
    0. 博客主要业务逻辑视图
"""

from django.http.response import JsonResponse, Http404
from django.views.generic import View
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model

from ljx.views import OpenView
from db import models as m
from db.utils import ContextUtil

from ljx import settings

User = get_user_model()


class DoingView(OpenView):
    """
    先占个坑
    """

    def get(self, request, *args, **kwargs):
        self.request.user.set_password()
        return render(request, 'doing.html')


class Detail(View):
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
        return self.model.objects.filter(is_active=True, author=obj.author).order_by('-add')[:10]

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
            'liked': self.get_art_like_status(pk),
        }
        # 更新阅读次数
        obj.read += 1
        obj.save(update_fields=('read',))
        return render(request, 'detail.html', ctx)

    def post(self, request, pk):
        obj = self.get_obj(pk)
        obj.like += 1
        obj.save(update_fields=['like', ])
        response = JsonResponse({'code': 0, 'msg': obj.like})
        # 7天内不允许重复点赞
        response.set_cookie(pk, 'true', expires=60 * 60 * 24 * 7)
        return response

    def get_art_like_status(self, pk):
        # 检验当前文章是否已经点赞过
        liked = self.request.COOKIES.get(pk, 'false')
        return liked


class Link(View):
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


class LinkAdd(View):
    """
    提交链接
    """

    def get(self, request, *args, **kwargs):
        html = render_to_string('linkform.html', {}, request)
        response = JsonResponse({'code': 0, 'text': html})
        return response

    def post(self, request, *args, **kwargs):
        email = self.request.POST.get('email')
        name = self.request.POST.get('link_name')
        link = self.request.POST.get('link')
        existed = m.Link.objects.filter(link=link).only(*('pk',)).count()
        if existed:
            return JsonResponse({'code': -1, 'msg': '链接已经在友链中！'})
        if not all((email, name, link)):
            return JsonResponse({'code': -2, 'msg': 'nothing to do'})
        try:
            m.Link.objects.create(link=link, email=email, link_name=name)
        except:
            pass
        return JsonResponse({'code': 0, 'msg': '提交成功，站长审核通过即可展示'})


class Message(View):
    """
    留言板
    """

    def get(self, request, *args, **kwargs):
        ctx = {
            'declare': '天涯何处觅知音！',
            'desc': '欢迎前来找我聊人生、聊理想、聊家常、谈天说地！',
            'page': {
                'title': '站点留言板',
                'keywords': '留言板、谈天说地',
                'description': '天涯何处觅知音？',
            }
        }
        return render(request, 'msg.html', ctx)


class DsImg(View):
    # 获取文章打赏码

    def get(self, request, *args, **kwargs):
        art_id = self.request.GET.get('art_id', 'xxx')
        art = m.Blog.objects.filter(pk=art_id).first()
        alipay_src = ''
        wechat_src = ''
        if not art:
            # 放上站长的二维码
            siter = User.objects.filter(email='jeeyshe@gmail.com').first()
            alipay_src = '{}{}'.format(settings.MEDIA_URL, siter.alipay)
            wechat_src = '{}{}'.format(settings.MEDIA_URL, siter.wechat)
        else:
            # 放上作者的二维码
            alipay_src = '{}{}'.format(settings.MEDIA_URL, art.author.alipay)
            wechat_src = '{}{}'.format(settings.MEDIA_URL, art.author.wechat)
        response = JsonResponse({
            "title": "作者打赏码",
            "id": 'dsm',
            "start": 0,
            "data": [
                {
                    "alt": "支付宝打赏码",
                    "pid": 'alipay',
                    "src": alipay_src,
                    "thumb": alipay_src
                },
                {
                    "alt": "微信打赏码",
                    "pid": 'wehcat',
                    "src": wechat_src,
                    "thumb": wechat_src
                },
            ]
        })
        return response


class GoTo(View):
    """
    友链或广告点击
    """

    def get(self, request, *args, **kwargs):
        return JsonResponse({'msg': 'OK'})


class Notice(View):
    """
    公告详情页
    """

    def get(self, request, pk, *args, **kwargs):
        obj = m.Notice.objects.filter(is_active=True, pk=pk).first()
        if not obj:
            raise Http404()
        ctx = {
            'tip': obj,
            'notices': m.Notice.objects.filter(is_active=True).order_by('-add').only(*('id', 'title'))
        }
        return render(request, 'notice.html', ctx)


class CatList(View):
    """
    TODO: 分类列表页
    """


class TagList(View):
    """
    TODO: 标签列表页
    """
    pass
