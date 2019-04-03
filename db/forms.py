# coding: utf-8
"""
Created by Jeeyshe.Ru at 2019/3/31 下午10:07, for any more contact me with jeeyshe@gmail.com.
Here is the descriptions and some purpose of the file:
    0. 自定义的表单
"""

from DjangoUeditor.forms import UEditorField, UEditorModelForm
from db import models


class CommentForm(UEditorModelForm):
    """
    提供给已登录游客的编辑器
    """
    content = UEditorField(
        required=True,
        label='',
        max_length=300,
        width='100%',
        height=200,
        imagePath='com/v/',
        toolbars='normal',
        settings={
            'wordCount': '',
            'initialContent': '文明上网，文明发言！',
            'autoClearinitialContent': 'true',
        },
    )

    class Meta:
        model = models.Comment
        fields = ('content',)
