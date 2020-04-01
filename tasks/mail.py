#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 邮件异步任务
"""
import os
import logging

import celery
from django.core.mail import send_mail, send_mass_mail
from django.core.mail import EmailMultiAlternatives
from django.template import loader

from ishare.settings import EMAIL_SUBJECT_PREFIX, SERVER_EMAIL


logger = logging.getLogger(__name__)


@celery.task(name='tasks.mail.test_mail')
def test_mail():
    subject = '{}这是一封测试邮件，邀你共赏美文《青春》'.format(EMAIL_SUBJECT_PREFIX)
    text_content = """
    青春不是年华，而是心境；青春不是桃面、丹唇、柔膝，而是深沉的意志、恢宏的想像、炽热的感情；青春是生命的深泉涌流。

    青春气贯长虹，勇锐盖过怯弱，进取压倒苟安。如此锐气，二十后生有之，六旬男子则更多见。年岁有加，并非垂老；理想丢弃，方堕暮年。

    岁月悠悠，衰微只及肌肤；热忱抛却，颓唐必致灵魂。忧烦、惶恐、丧失自信，定使心灵扭曲，意气如灰。

    无论年届花甲，抑或二八芳龄，心中皆有生命之欢乐，奇迹之诱惑，孩童般天真久盛不衰。人的心灵应如浩淼瀚海，只有不断接纳美好、希望、欢乐、勇气和力量的百川，才能青春永驻、风华长存。

    一旦心海枯竭，锐气便被冰雪覆盖，玩世不恭、自暴自弃油然而生，即使年方二十，实已垂垂老矣；然则只要虚怀若谷，让喜悦、达观、仁爱充盈其间，你就有望在八十高龄告别尘寰时仍觉年轻。
    """
    # html_content = '<p>这是一封<strong>重要的</strong>邮件.</p>'
    msg = EmailMultiAlternatives(subject, text_content, SERVER_EMAIL, ['support@lujianxin.com'])
    # msg.attach_alternative(html_content, "text/html")
    msg.send()


@celery.task(name="tasks.mail.send_one")
def send_one(subject, message, recipient_list, html=None):
    """
    发送一条消息: 自动添加主题前缀和签名
    """
    send_mail(
        subject='{}{}'.format(EMAIL_SUBJECT_PREFIX, subject),
        message=message,
        from_email=SERVER_EMAIL,
        recipient_list=recipient_list,
        html_message=html,
    )


@celery.task(name="tasks.mail.send_many")
def send_many(datatuple):
    """
    一次性发送多条消息: 自动添加前缀和主题签名
    datatuple:
    (
        (subject0, message0, sender, recipient),
        (subject1, message1, sender, recipient),
        (subject2, message2, sender, recipient),
    )
    """
    send_mass_mail(datatuple)


@celery.task(name="tasks.mail.send_password_reset_link")
def send_password_rest_link(subject_template_name, email_template_name,
                            context, from_email, to_email, html_email_template_name=None):
    subject = loader.render_to_string(subject_template_name, context)
    subject = ''.join(subject.splitlines())
    subject = '{}{}'.format(EMAIL_SUBJECT_PREFIX, subject)
    body = loader.render_to_string(email_template_name, context)
    email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
    if html_email_template_name is not None:
        html_email = loader.render_to_string(html_email_template_name, context)
        email_message.attach_alternative(html_email, 'text/html')
    email_message.send()
