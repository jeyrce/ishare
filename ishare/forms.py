# coding: utf-8
"""
Created by Jeyrce.Lu 2020/4/1 下午10:24, contact with jeyrce@gmail.com or website https://www.lujianxin.com
---------------------------------------------------------------------------------------------------------
>>> 表单文件
"""

from django.contrib.auth.forms import PasswordResetForm

from tasks.mail import send_password_rest_link


class SyncMailPasswordResetForm(PasswordResetForm):
    """
    覆盖父类同步发送邮件,此处使用异步任务
    """

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email,
                  html_email_template_name=None):
        send_password_rest_link.delay(subject_template_name, email_template_name, context, from_email, to_email,
                                      html_email_template_name=None)
