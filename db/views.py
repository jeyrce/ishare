# coding: utf-8
"""
Created by Jeeyshe.Ru at 19-3-27 下午7:22, for any more contact me with jeeyshe@gmail.com.
Here is the descriptions and some purpose of the file:
    0. 博客主要业务逻辑视图
"""

from django.http.response import JsonResponse, HttpResponse, Http404
from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password

from ljx.views import OpenView
from db import models as m
from db.utils import ContextUtil, make_auth_token
from db.forms import CommentForm

from ljx import settings


class DoingView(OpenView):
    """
    先占个坑
    """

    def get(self, request, *args, **kwargs):
        return render(request, 'doing.html')


class ArticleObj(View):
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
            'cform': CommentForm(),
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

    def patch(self, request, pk):
        # 修改文章
        return JsonResponse({"code": 0, "msg": 'put xxx'})

    def delete(self, request, pk):
        # 删除文章
        obj = self.get_obj(pk)
        obj.is_active = False
        obj.save(update_fields=['is_active', ])
        return JsonResponse({"code": 0, "msg": obj.pk})

    def get_art_like_status(self, pk):
        # 检验当前文章是否已经点赞过
        liked = self.request.COOKIES.get(pk, 'false')
        return liked


class ArticleAdd(View):

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


class Message(View):
    """
    留言板
    """

    def get(self, request, *args, **kwargs):
        print(kwargs)
        ctx = {

        }
        return render(request, 'msg.html', ctx)


class SignIn(View):

    def get(self, request, *args, **kwargs):
        # 获取接下来要去的地方
        next = self.request.META.get('HTTP_REFERER', '/')
        return render(request, 'auth/signin.html', {'next': next})

    def post(self, request, *args, **kwargs):
        # 进行登录
        obj = m.Visitor.objects.filter(email=self.request.POST.get('email')).first()
        if not obj:
            return JsonResponse({'msg': '账号不存在', 'code': -1})
        if not obj.is_active:
            return JsonResponse({'msg': '账号被冻结', 'code': -2})
        if not check_password(self.request.POST.get('pwd'), obj.pwd):
            return JsonResponse({'msg': '密码不正确', 'code': -3})
        auth_token = make_auth_token(obj, settings.SECRET_KEY)
        response = JsonResponse({'msg': 'ok', 'code': 0})
        self.request.session['auth_token'] = auth_token
        return response

    def delete(self, request, *args, **kwargs):
        # 注销登录
        raise NotImplementedError()


class DsImg(View):
    # 获取文章打赏码

    def get(self, request, *args, **kwargs):
        art_id = self.request.GET.get('art_id', 'xxx')
        art = m.Blog.objects.filter(pk=art_id).first()
        alipay_src = ''
        wechat_src = ''
        if not art:
            # 放上站长的二维码
            siter = m.Visitor.objects.filter(pk='jeeyshe@gmail.com').first()
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
