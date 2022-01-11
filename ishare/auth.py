# coding: utf-8
"""
Created by Jeyrce.Lu 2020/4/1 下午8:45, contact with jeyrce@gmail.com or website https://www.lujianxin.com
---------------------------------------------------------------------------------------------------------
>>> 本站登录认证方式
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.views import PasswordResetView
from django.views import View
from django.http.response import HttpResponse

from ishare import settings as _st
from ishare.forms import SyncMailPasswordResetForm

UserAccount = get_user_model()


class SyncMailPasswordResetView(PasswordResetView):
    """
    cover原有逻辑, 采用异步任务发送邮件
    """
    form_class = SyncMailPasswordResetForm


class EmailAuthBackend(ModelBackend):
    """
    使用email作为账户登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username
        try:
            account = UserAccount.objects.get(**{UserAccount.EMAIL_FIELD: email})
        except UserAccount.DoesNotExist:
            pass
        else:
            if account.check_password(password) and self.user_can_authenticate(account):
                if _st.UPGRADING:
                    if not account.is_superuser:
                        # 维护期间不允许作者登录
                        account.is_staff = False
                return account


class QQAuthBackend(ModelBackend):
    """
    使用qq第三方登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        pass


class GithubAuthBackend(ModelBackend):
    """
    使用github第三方登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        pass


class WechatAuthBackend(ModelBackend):
    """
    使用微信第三方登录
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        pass
