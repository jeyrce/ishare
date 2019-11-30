# coding: utf-8
"""
Created by Jeeyshe.Ru at 19-3-27 下午7:20, for any more contact me with jeeyshe@gmail.com.
Here is the descriptions and some purpose of the file:
    0. 博客主要业务逻辑路由
"""

from django.urls import path

from db import views

app_name = 'db'

urlpatterns = [

    path('art/<pk>', views.Detail.as_view()),  # 文章详情页

    path('link.html', views.Link.as_view()),  # 友链页

    path('msg.html', views.Message.as_view()),  # 留言留言列表页

    path('art/dsm/', views.DsImg.as_view()),  # 获取打赏码地址

    path('cat/<pk>/', views.CatList.as_view()),  # 某类别文章列表

    path('tag/<pk>/', views.TagList.as_view()),  # 某标签文章列表

    path('notice/<pk>', views.Notice.as_view()),  # 公告详情页

    path('goto/', views.GoTo.as_view()),  # 友链点击记录

    path('link/add', views.LinkAdd.as_view()),  # 提交友链

    path('search/', views.SearchView.as_view()),  # 站内搜索
]
