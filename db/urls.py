# coding: utf-8
"""
Created by Jeeyshe.Ru at 19-3-27 下午7:20, for any more contact me with jeeyshe@gmail.com.
Here is the descriptions and some purpose of the file:
    0. 博客主要业务逻辑路由
"""

from django.urls import path, re_path

from db import views

app_name = 'db'

urlpatterns = [
    # ----------------------------------------------页面类
    # 文章详情页
    path('art/<pk>', views.ArticleObj.as_view()),
    # 文学类列表页
    path('soul.html', views.Soul.as_view()),
    # 友链页
    path('link.html', views.Link.as_view()),
    # 某类别文章列表
    path('cat/<pk>', views.DoingView.as_view()),
    # 某标签文章列表
    path('tag/<pk>', views.DoingView.as_view()),
    # 留言留言列表页
    path('msg.html', views.DoingView.as_view()),
    # 投稿页面，在线编辑
    path('write.html', views.DoingView.as_view()),
    # 作者主页
    path('me.html', views.DoingView.as_view()),
    # 对外作者主页
    path('author/<nickname>', views.DoingView.as_view()),

    # --------------------------------------------接口类
    # 认证
    path('auth', views.DoingView.as_view()),
    path('comment/add', views.CommentAdd.as_view()),
    # 广告或友链点击记录
    path('goto', views.DoingView.as_view()),
    # 登录页面
    path('signin', views.DoingView.as_view()),
    # 注册页面
    path('signup', views.DoingView.as_view()),
    # 登出
    path('signout', views.DoingView.as_view()),
]
