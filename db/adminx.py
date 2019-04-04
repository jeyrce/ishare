# coding: utf-8
"""
Created by Lu Jianxin at 2019/03/10 23:06, for any questions contact me with jeeysie@gmail.com.
Some ideas of the file:
    0. 后台管理系统配置
"""
from django.contrib.auth.views import get_user_model
from django.utils.translation import ugettext as _

import xadmin
from xadmin import views
from xadmin.layout import Main, Fieldset, Row, Side, Col
from db.models import (
    Tag,
    Category,
    Visitor,
    Blog,
    TopBlog,
    Comment,
    Message,
    Advertisement,
    TipAd,
    AdClick,
    Link,
    Click,
    Notice,
    Expand,
)

User = get_user_model()


# ----------------------全局配置----------------------
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = '博客后台管理系统'
    site_footer = '陆鉴鑫的博客'
    menu_style = 'accordion'  # 还有一个选项default
    global_search_models = (Tag, User)
    global_add_models = (
        User,
        Tag,
        Category,
        Blog,
        TopBlog,
        Advertisement,
        TipAd,
        Link,
        Notice,
        Expand,
    )


class CommonSetting(object):
    refresh_times = (5, 10, 30, 60)
    ordering = ('-add',)
    list_per_page = 60
    empty_value_display = '-暂无-'
    list_gallery = True
    use_related_menu = False
    style_fields = {'content': 'ueditor', 'reply': 'ueditor'}
    # relfield_style = 'fk_ajax'  # ajax加载外键选项


# --------------------模块设置----------------------

class TagAdmin(CommonSetting):
    list_display = ('tag', 'is_active', 'art_nums', 'add', 'mod')
    search_fields = ('tag',)
    list_filter = ('add', 'mod', 'is_active')
    readonly_fields = ('add', 'mod')
    list_editable = ('tag', 'is_active')
    form_layout = (
        Main(
            Fieldset(
                _("标签信息"),
                Row('tag', 'art_nums'),
                Row('add', 'mod'),
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active'),
        ),
    )

    # def queryset(self):
    #     """
    #     重写查询展示列表页
    #     """
    #     q = super().queryset()
    #     nq = q.filter()
    #     return nq
    #
    # def save_models(self):
    #     """
    #     保存实例时要做的事
    #     """
    #     super().save_models()


class CateGoryAdmin(CommonSetting):
    list_display = ('cat', 'is_active', 'art_nums', 'add', 'mod')
    search_fields = ('cat',)
    list_filter = ('add', 'mod', 'is_active')
    readonly_fields = ('add', 'mod')
    list_editable = ('cat', 'is_active')
    form_layout = (
        Main(
            Fieldset(
                _('类别信息'),
                Row('cat', 'art_nums'),
                Row('add', 'mod')
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active'),
        ),
    )


class VisitorAdmin(CommonSetting):
    list_display = ('id', 'is_active', 'is_author', 'nickname')
    search_fields = ('id', 'nickname', 'desc')
    list_filter = ('is_author', 'is_active')
    readonly_fields = ('add', 'mod')
    list_editable = ('is_active', 'is_author')
    exclude = ('pwd',)
    form_layout = (
        Main(
            Fieldset(
                _('基本信息'),
                Row('id', 'nickname'),
                Row('header'),
                Row('add', 'mod'),
            ),
            Fieldset(
                _('打赏账户'),
                Row('alipay', 'wechat'),
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active', 'is_author'),
            Fieldset(_('简介'), 'desc')
        )
    )

    def has_add_permission(self):
        if self.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request=None, obj=None):
        if self.user.is_superuser:
            return True
        return False


class BlogAdmin(CommonSetting):
    exclude = ('id',)
    list_display = ('title', 'author', 'cat', 'original', 'tags', 'read', 'like', 'com', 'url')
    search_fields = ('title', 'author__nickname', 'author__id')
    list_filter = ('is_active', 'add', 'mod')
    readonly_fields = ('read', 'like', 'add', 'mod')
    list_editable = ('title', 'cat', 'is_fine', 'is_top', 'is_active')
    form_layout = (
        Main(
            Fieldset(
                _('基本信息'),
                Row('title', 'author'),
                Row('cat', 'tags'),
                Row('cover'),
            ),
            Fieldset(
                _('正文'),
                Row('source'),
                Row('content'),
            ),
            Fieldset(
                _('统计信息'),
                Row('read', 'like'),
                Row('add', 'mod'),
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active', 'is_top', 'is_fine'),
        )
    )

    def queryset(self):
        q = super().queryset()
        return q.filter(is_top=False)


class TopBlogAdmin(CommonSetting):
    """
    置顶文章管理
    """
    exclude = ('id',)
    list_display = ('title', 'author', 'cat', 'original', 'tags', 'read', 'like', 'com', 'url')
    search_fields = ('title', 'author__nickname', 'author__id')
    list_filter = ('is_active', 'add', 'mod')
    readonly_fields = ('read', 'like', 'add', 'mod')
    list_editable = ('title', 'cat', 'is_fine', 'is_top', 'is_active')
    form_layout = (
        Main(
            Fieldset(
                _('基本信息'),
                Row('title', 'author'),
                Row('cat', 'tags'),
                Row('cover'),
            ),
            Fieldset(
                _('正文'),
                Row('source'),
                Row('content'),
            ),
            Fieldset(
                _('统计信息'),
                Row('read', 'like'),
                Row('add', 'mod'),
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active', 'is_top', 'is_fine'),
        )
    )

    def queryset(self):
        q = super().queryset()
        return q.filter(is_top=True)


class CommentAdmin(CommonSetting):
    list_display = ('__str__', 'is_active', 'obj_type', 'blog', 'add')
    search_fields = ()
    list_filter = ('is_active', 'add')
    readonly_fields = ('add', 'rep')
    list_editable = ('is_active',)
    form_layout = (
        Main(
            Fieldset(
                _('访客对象'),
                Row('visitor'),
                Row('nickname', 'email')
            ),
            Fieldset(
                _('评论信息'),
                Row('blog', 'add'),
                Row('content'),
            ),
            Fieldset(
                _('作者回复'),
                Row('reply'),
                Row('rep'),
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active'),
        )
    )


class MessageAdmin(CommonSetting):
    list_display = ('__str__', 'obj_type', 'is_active', 'add')
    search_fields = ()
    list_filter = ('add', 'is_active')
    readonly_fields = ('add', 'rep')
    list_editable = ('is_active',)
    form_layout = (
        Main(
            Fieldset(
                _('访客对象'),
                Row('visitor', ),
                Row('nickname', 'email'),
            ),
            Fieldset(
                _('留言信息'),
                Row('content'),
                Row('add'),
            ),
            Fieldset(
                _('回复信息'),
                Row('reply'),
                Row('rep'),
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active')
        )
    )


class AdvertisementAdmin(CommonSetting):
    list_display = ('ad_name', 'adtype', 'url', 'end')
    search_fields = ('ad_name', 'remark')
    list_filter = ('add', 'mod', 'end')
    readonly_fields = ('add', 'mod')
    list_editable = ('end',)
    form_layout = (
        Main(
            Fieldset(
                _('广告信息'),
                Row('ad_name', 'add', 'end'),
                Row('link', 'mod'),
                Row('image', 'adtype')
            ),
        ),
        Side(
            Fieldset(_('备注'), 'remark')
        )
    )

    def queryset(self):
        q = super().queryset()
        return q.filter(adtype=0)


class TipAdAdmin(CommonSetting):
    list_display = ('ad_name', 'adtype', 'url', 'end')
    search_fields = ('ad_name', 'remark')
    list_filter = ('add', 'mod', 'end')
    readonly_fields = ('add', 'mod')
    list_editable = ('end',)
    form_layout = (
        Main(
            Fieldset(
                _('广告信息'),
                Row('ad_name', 'add', 'end'),
                Row('link', 'mod'),
                Row('image', 'adtype')
            ),
        ),
        Side(
            Fieldset(_('备注'), 'remark')
        )
    )

    def queryset(self):
        q = super().queryset()
        return q.filter(adtype=1)


class AdClickAdmin(CommonSetting):
    list_display = ('advertisement', 'ip', 'add')
    search_fields = ('advertisement__ad_name',)
    list_filter = ('add',)
    readonly_fields = ('add', 'user_agent')
    list_editable = ()
    form_layout = (
        Main(
            Fieldset(
                _('广告主体'),
                Row('advertisement')
            ),
            Fieldset(
                _('ip记录'),
                Row('ip', 'add'),
                Row('user_agent')
            ),
        ),
    )


class LinkAdmin(CommonSetting):
    list_display = ('link_name', 'is_active', 'cat', 'url')
    search_fields = ('link_name', 'email', 'link')
    list_filter = ('add', 'mod', 'is_active')
    readonly_fields = ('add', 'mod')
    list_editable = ('is_active', 'cat')
    form_layout = (
        Main(
            Fieldset(
                _('链接信息'),
                Row('link_name', 'cat'),
                Row('link', 'email'),
                Row('add', 'mod')
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active'),
        )
    )


class ClickAdmin(CommonSetting):
    list_display = ('link', 'ip', 'add')
    search_fields = ('link__link_name',)
    list_filter = ('add',)
    readonly_fields = ('add', 'user_agent')
    list_editable = ()
    form_layout = (
        Main(
            Fieldset(
                _('友链主体'),
                Row('link')
            ),
            Fieldset(
                _('ip记录'),
                Row('ip', 'add'),
                Row('user_agent')
            ),
        ),
    )


class NoticeAdmin(CommonSetting):
    list_display = ('title', 'is_active', 'add', 'url')
    search_fields = ('title',)
    list_filter = ('add', 'mod', 'is_active')
    readonly_fields = ('add', 'mod')
    list_editable = ('is_active',)
    form_layout = (
        Main(
            Fieldset(
                _('公告信息'),
                Row('title'),
                Row('add', 'mod'),
                Row('content')
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active')
        )
    )


class ExpandAdmin(CommonSetting):
    list_display = ('key', 'value')
    search_fields = ('remark', 'key')
    list_filter = ('mod',)
    ordering = ('-mod',)
    readonly_fields = ('mod',)
    list_editable = ()
    form_layout = (
        Main(
            Fieldset(
                _('数据记录'),
                Row('key'),
                Row('value'),
                Row('mod')
            )
        ),
        Side(
            Fieldset(_('备注'), 'remark')
        )
    )


# ---------------------注册--------------------
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Category, CateGoryAdmin)
xadmin.site.register(Visitor, VisitorAdmin)
xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(TopBlog, TopBlogAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(Message, MessageAdmin)
xadmin.site.register(Advertisement, AdvertisementAdmin)
xadmin.site.register(TipAd, TipAdAdmin)
xadmin.site.register(AdClick, AdClickAdmin)
xadmin.site.register(Link, LinkAdmin)
xadmin.site.register(Click, ClickAdmin)
xadmin.site.register(Notice, NoticeAdmin)
xadmin.site.register(Expand, ExpandAdmin)

xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
