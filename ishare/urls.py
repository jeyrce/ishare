"""ishare URL Configuration

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
from django.contrib.auth import views as auth_views

from ishare import views
from ishare.auth import SyncMailPasswordResetView, SendOne
from ishare.settings import MEDIA_ROOT

# ==============前台展示系统路由==============
urlpatterns = [
    path('', views.Index.as_view(), name='index'),  # 首页
    path('index', views.goto_index),
    path('index.html', views.goto_index),
    path('feed.html', views.ArticleFeed()),  # RSS订阅
    path('feed', views.ArticleFeed()),  # RSS订阅
    path('rss', views.ArticleFeed()),  # RSS订阅
    path('rss.html', views.ArticleFeed()),  # RSS订阅
    path('sitemap.xml', sitemap, views.sitemaps, name='django.contrib.sitemaps.views.sitemap'),  # sitemap
]

# ==============文件处理路由==============
urlpatterns.extend([
    re_path('^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    path('ueditor/', include('DjangoUeditor.urls')),
])

# ===============后台管理路由================
urlpatterns.extend([
    path('admin/', admin.site.urls),
])

# =============博客业务路由=============
urlpatterns.extend([
    path('x/', include('blog.urls', namespace='x')),
])

# ===============认证部分路由=============
urlpatterns.extend([
    path('auth/password_reset/', SyncMailPasswordResetView.as_view(), name='password_reset'),
    path('auth/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('auth/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('auth/sendone/', SendOne.as_view())
])
