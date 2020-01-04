"""ljx URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path, include
from django.views.static import serve
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

import xadmin
from xadmin.plugins import xversion

from ljx import views
from ljx.settings import MEDIA_ROOT

xadmin.autodiscover()
xversion.register_models()

urlpatterns = [
    # 后台管理系统
    path('xauth/', xadmin.site.urls),
    path('admin/', admin.site.urls),
    path('xauth/db/author/<uid>/password/', views.password_reset),
    # 其他
    re_path('^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    path('ueditor/', include('DjangoUeditor.urls')),
    # 前台展示系统
    path('', views.Index.as_view(), name='index'),
    path('index', views.goto_index),
    path('index.html', views.goto_index),
    path('feed.html', views.ArticleFeed()),  # RSS订阅
    path('feed', views.ArticleFeed()),  # RSS订阅
    path('rss', views.ArticleFeed()),  # RSS订阅
    path('rss.html', views.ArticleFeed()),  # RSS订阅
    path('sitemap.xml', sitemap, views.sitemaps, name='django.contrib.sitemaps.views.sitemap'),  # sitemap
    # 业务逻辑模块
    path('x/', include('db.urls', namespace='x')),
]
