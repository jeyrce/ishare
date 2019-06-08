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
from xadmin.plugins.auth import UserAdmin
from db.models import (
    Music,
    Tag,
    Category,
    Blog,
    AuthorBlog,
    Author,
    Book,
    AuthorBook,
    Chapter,
    AuthorChapter,
    Advertisement,
    TipAd,
    Link,
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
    global_search_models = ()
    global_add_models = ()


class CommonSetting(object):
    refresh_times = (5, 10, 30, 60)
    ordering = ('-add',)
    list_per_page = 60
    empty_value_display = '-暂无-'
    list_gallery = True
    list_editable = ()
    use_related_menu = False
    style_fields = {'content': 'ueditor'}
    # relfield_style = 'fk_ajax'  # ajax加载外键选项


# --------------------模块设置----------------------
class MusicAdmin(CommonSetting):
    list_display = ('name', 'is_active', 'author', 'mod', 'art_nums')
    search_fields = ('name', 'author')
    list_filter = ('is_active',)
    readonly_fields = ('mod',)
    ordering = ('pk',)
    form_layout = (
        Main(
            Fieldset(
                _("音乐信息"),
                Row('name', 'author'),
                Row('file'),
                Row('mod'),
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active'),
        ),
    )


class TagAdmin(CommonSetting):
    list_display = ('tag', 'is_active', 'art_nums', 'add', 'mod')
    search_fields = ('tag',)
    list_filter = ('add', 'mod', 'is_active')
    readonly_fields = ('add', 'mod')
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


class CategoryAdmin(CommonSetting):
    list_display = ('pre_cat', 'cat', 'is_active', 'art_nums', 'add', 'mod')
    search_fields = ('cat', 'pre_cat')
    list_filter = ('add', 'mod', 'is_active')
    readonly_fields = ('add', 'mod')
    form_layout = (
        Main(
            Fieldset(
                _('类别信息'),
                Row('pre_cat', 'cat'),
                Row('add', 'mod')
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active'),
        ),
    )


class UserAccountAdmin(CommonSetting, UserAdmin):
    change_user_password_template = None
    list_display = ('email', 'username', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')
    exclude = ('last_name', 'first_name')
    style_fields = {'user_permissions': 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset(_('Personal info'),
                             Row('email'),
                             Row('password'),
                             ),
                    Fieldset(
                        '作者信息',
                        Row('username', 'header'),
                        Row('desc'),
                        Row('alipay', 'wechat'),
                    ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             Row('last_login', 'date_joined')
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()

    def save_models(self):
        if self.new_obj.email is None:
            self.new_obj.email = 'author@lujianxin.com'
        self.new_obj.save()


class AuthorAdmin(CommonSetting, UserAdmin):
    """
    作者的管理类
    """
    change_user_password_template = None
    list_display = ('email', 'username', 'is_staff', 'is_active')
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login', 'email', 'is_active', 'is_staff', 'is_superuser')
    exclude = ('last_name', 'first_name', 'groups', 'user_permissions')
    style_fields = {'user_permissions': 'm2m_transfer'}
    model_icon = 'fa fa-user'
    relfield_style = 'fk-ajax'

    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset(_('Personal info'),
                             Row('email'),
                             Row('password'),
                             ),
                    Fieldset(
                        '作者信息',
                        Row('username', 'header'),
                        Row('desc'),
                        Row('alipay', 'wechat'),
                    ),
                    Fieldset(_('Important dates'),
                             Row('last_login', 'date_joined')
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()

    def queryset(self):
        q = super().queryset()
        return q.filter(id=self.request.user.id)

    def has_delete_permission(self, obj=None):
        # 删除权限
        return False

    def has_add_permission(self):
        return False

    def save_models(self):
        if self.new_obj.email is None:
            self.new_obj.email = 'author@lujianxin.com'
        self.new_obj.save()

    def has_change_permission(self, obj=None):
        if obj is not None:
            if self.request.user.id == obj.id:
                return True


class BlogAdmin(CommonSetting):
    exclude = ('id',)
    list_display = ('title', 'author', 'cat', 'original', 'tags', 'read', 'like', 'url')
    search_fields = ('title', 'author__nickname', 'author__email')
    list_filter = ('is_active', 'add', 'mod')
    readonly_fields = ('read', 'like', 'add', 'mod')
    form_layout = (
        Main(
            Fieldset(
                _('基本信息'),
                Row('title', 'cat', 'author'),
                Row('cover', 'tags'),
                Row('music')
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

    def save_models(self):
        """
        保存数据到数据库中时提取作者为当前用户
        """
        if (not hasattr(self.new_obj, 'author')) or (not self.new_obj.author):
            self.new_obj.author = self.request.user
        self.new_obj.save()


class AuthorBlogAdmin(CommonSetting):
    exclude = ('id', 'author')
    list_display = ('title', 'cat', 'original', 'tags', 'read', 'like', 'url')
    search_fields = ('title',)
    list_filter = ('add', 'mod')
    readonly_fields = ('read', 'like', 'add', 'mod', 'is_active', 'is_top', 'is_fine')
    form_layout = (
        Main(
            Fieldset(
                _('基本信息'),
                Row('title', 'cat'),
                Row('cover', 'tags'),
                Row('music')
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
            Fieldset(_('状态'), 'is_active', 'is_top', 'is_fine')
        )
    )

    def queryset(self):
        q = super().queryset()
        return q.filter(author_id=self.request.user.id)

    def save_models(self):
        """
        01.保存数据到数据库中时提取作者为当前用户
        02.修复代码块bug
        """
        if (not hasattr(self.new_obj, 'author')) or (not self.new_obj.author):
            self.new_obj.author = self.request.user
        self.new_obj.save()

    def has_add_permission(self):
        # 写文章的权限
        if self.request.user.is_superuser:
            return True
        return self.request.user.is_active

    def has_delete_permission(self, obj=None):
        # 删除权限
        if obj is not None:
            if self.request.user.id == obj.author.id:
                return True

    def has_change_permission(self, obj=None):
        if obj is not None:
            if self.request.user.id == obj.author.id:
                return True


class BookAdmin(CommonSetting):
    """
    专题管理
    """
    list_display = ('bname', 'is_active', 'author', 'cat', 'read', 'cnum', 'last_update')
    search_fields = ('bname',)
    list_filter = ('add', 'mod')
    exclude = ('id',)
    readonly_fields = ('read', 'add', 'mod')
    use_related_menu = True
    form_layout = (
        Main(
            Fieldset(
                _('基本信息'),
                Row('bname'),
                Row('author'),
            ),
            Fieldset(
                _('描述信息'),
                Row('cat', 'tags'),
                Row('cover'),
                Row('desc'),
            ),
            Fieldset(
                _('统计信息'),
                Row('read', 'add', 'mod'),
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active', 'is_fine'),
        ),
    )

    def save_models(self):
        """
        保存数据到数据库中时提取作者为当前用户
        """
        if (not hasattr(self.new_obj, 'author')) or (not self.new_obj.author):
            self.new_obj.author = self.request.user
        self.new_obj.save()


class ChapterInline(object):
    """
    专题内查看编辑章节
    """
    model = Chapter
    extra = 0
    exclude = ('id', 'is_active')
    can_delete = False
    show_change_link = True


class AuthorBookAdmin(CommonSetting):
    """
    作者专题管理
    """
    list_display = ('bname', 'is_active', 'cnum', 'read', 'last_update')
    inlines = (ChapterInline,)
    search_fields = ('bname',)
    list_filter = ('add', 'mod')
    exclude = ('id', 'author')
    readonly_fields = ('is_active', 'is_fine', 'read', 'add', 'mod')

    form_layout = (
        Main(
            Fieldset(
                _('基本信息'),
                Row('bname'),
            ),
            Fieldset(
                _('描述信息'),
                Row('cat', 'tags'),
                Row('cover'),
                Row('desc'),
            ),
            Fieldset(
                _('统计信息'),
                Row('read', 'add', 'mod'),
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active', 'is_fine'),
        ),
    )

    def queryset(self):
        q = super().queryset()
        return q.filter(author_id=self.request.user.id)

    def save_models(self):
        """
        保存数据到数据库中时提取作者为当前用户
        """
        self.new_obj.author = self.request.user
        self.new_obj.save()

    def has_add_permission(self):
        # 增添专题的权限
        if self.request.user.is_superuser:
            return True
        return self.request.user.is_active

    def has_delete_permission(self, obj=None):
        # 删除权限
        if obj is not None:
            if self.request.user.id == obj.author.id:
                return True

    def has_change_permission(self, obj=None):
        if obj is not None:
            if self.request.user.id == obj.author.id:
                return True


class ChapterAdmin(CommonSetting):
    """
    章节
    """
    list_display = ('title', 'book', 'is_active', 'add')
    search_fields = ('title',)
    list_filter = ('book__bname',)
    exclude = ('id',)
    readonly_fields = ('add', 'mod')
    form_layout = (
        Main(
            Fieldset(
                _('基本信息'),
                Row('title'),
                Row('book'),
            ),
            Fieldset(
                _('正文'),
                Row('content'),
            ),
            Fieldset(
                _('统计信息'),
                Row('add', 'mod'),
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active'),
        ),
    )

    def has_add_permission(self):
        # 此通道只允许管理员修改和查看
        return False

    def has_delete_permission(self, obj=None):
        # 删除权限
        return False

    def has_change_permission(self, obj=None):
        if obj is not None:
            if self.request.user.is_superuser:
                return True


class AuthorChapterAdmin(CommonSetting):
    """
    章节
    """
    list_display = ('title', 'book', 'is_active', 'add')
    search_fields = ('title',)
    list_filter = ('book__bname',)
    exclude = ('id',)
    readonly_fields = ('add', 'mod', 'is_active')
    form_layout = (
        Main(
            Fieldset(
                _('基本信息'),
                Row('title'),
                Row('book'),
            ),
            Fieldset(
                _('正文'),
                Row('content'),
            ),
            Fieldset(
                _('统计信息'),
                Row('add', 'mod'),
            ),
        ),
        Side(
            Fieldset(_('状态'), 'is_active'),
        ),
    )

    def has_add_permission(self):
        # 此通道只允许管理员修改和查看
        return True

    def has_delete_permission(self, obj=None):
        # 删除权限
        return False

    def has_change_permission(self, obj=None):
        if obj is not None:
            if self.request.user.is_superuser:
                return True
            if self.request.user.id == obj.author.id:
                return True


class AdvertisementAdmin(CommonSetting):
    list_display = ('ad_name', 'adtype', 'url', 'end')
    search_fields = ('ad_name', 'remark')
    list_filter = ('add', 'mod', 'end')
    readonly_fields = ('add', 'mod')
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


class LinkAdmin(CommonSetting):
    list_display = ('link_name', 'is_active', 'cat', 'url')
    search_fields = ('link_name', 'email', 'link')
    list_filter = ('add', 'mod', 'is_active')
    readonly_fields = ('add', 'mod')
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


class NoticeAdmin(CommonSetting):
    list_display = ('title', 'is_active', 'add', 'url')
    search_fields = ('title',)
    list_filter = ('add', 'mod', 'is_active')
    readonly_fields = ('add', 'mod')
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
xadmin.site.register(Music, MusicAdmin)
xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(User, UserAccountAdmin)
xadmin.site.register(Author, AuthorAdmin)
xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(AuthorBlog, AuthorBlogAdmin)
xadmin.site.register(Book, BookAdmin)
xadmin.site.register(AuthorBook, AuthorBookAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(AuthorChapter, AuthorChapterAdmin)
xadmin.site.register(Advertisement, AdvertisementAdmin)
xadmin.site.register(TipAd, TipAdAdmin)
xadmin.site.register(Link, LinkAdmin)
xadmin.site.register(Notice, NoticeAdmin)
xadmin.site.register(Expand, ExpandAdmin)

xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
