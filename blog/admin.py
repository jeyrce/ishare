from django.contrib import admin
from django.contrib.auth import get_user_model
# Register your models here.
from blog.models import (
    Music,
    Tag,
    Category,
    Blog,
    AuthorBlog,
    Author,
    Advertisement,
    Link,
    Notice,
    Expand,
)

Account = get_user_model()

admin.site.site_header = '后台管理系统'
admin.site.site_title = '陆鉴鑫的博客后台'


class CommenAdmin(admin.ModelAdmin):
    """
    公共的设置
    """
    pass


class MusicAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "is_active", "art_nums", "mod")
    list_editable = ("is_active",)
    list_per_page = 60
    readonly_fields = ("mod",)
    ordering = ("author",)
    search_fields = ("name", "author")
    list_filter = ("is_active",)
    empty_value_display = 'N/A'
    fieldsets = (
        ("主要信息", {"fields": ("name", "author", "is_active", ("code",))}),
        ("时间信息", {"fields": ("mod",)}),
    )


class TagAdmin(admin.ModelAdmin):
    list_display = ("tag", "is_active", "art_nums", "mod", "url")
    list_editable = ("is_active",)
    list_per_page = 60
    readonly_fields = ("mod", "add")
    ordering = ("-add",)
    search_fields = ("tag",)
    list_filter = ("is_active",)
    empty_value_display = 'N/A'
    fieldsets = (
        ("主要信息", {"fields": ("tag", "is_active",)}),
        ("时间信息", {"fields": ("mod", "add",)}),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("cat", "pre_cat", "is_active", "art_nums", "mod", "url")
    list_editable = ("is_active", "pre_cat")
    list_per_page = 60
    readonly_fields = ("mod", "add")
    ordering = ("-add",)
    search_fields = ("cat",)
    list_filter = ("pre_cat", "is_active")
    empty_value_display = 'N/A'
    fieldsets = (
        ("主要信息", {"fields": ("pre_cat", "cat", "is_active")}),
        ("时间信息", {"fields": ("mod", "add",)}),
    )


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', "is_active", 'author', 'cat', 'original', 'read', 'like', 'url')
    list_editable = ("is_active", "cat")
    list_per_page = 60
    readonly_fields = ("mod", "add", "read", "like")
    ordering = ("-add",)
    search_fields = ("title", "author__username", "author__email")
    list_filter = ("cat", "is_active")
    empty_value_display = 'N/A'
    fieldsets = (
        ("基本信息", {"fields": ("title", "cover", "author", "music", "cat", "tags",)}),
        ("标记信息", {"fields": ("is_active", "is_top", "is_fine")}),
        ("正文部分", {"fields": ("source", "content",)}),
        ("统计信息", {"fields": (("read", "like"), "mod", "add",)}),
    )

    def save_model(self, request, obj, form, change):
        # todo 新增文章时, 发邮件给站长, 提示站长进行审核
        # if not change: send_mail
        # 当没有作者时, 将当前登陆者作为作者
        if (not hasattr(obj, 'author')) or (not obj.author):
            obj.author = request.user
        obj.save()


class AuthorBlogAdmin(admin.ModelAdmin):
    list_display = ('title', "is_active", 'author', 'cat', 'original', 'read', 'like', 'url')
    list_editable = ("cat",)
    list_per_page = 60
    readonly_fields = ("mod", "add", "read", "like",
                       "is_active", "is_top", "is_fine", "apply_active", "apply_fine", "apply_top")
    ordering = ("-add",)
    search_fields = ("title", "author__username", "author__email")
    list_filter = ("cat", "is_active")
    empty_value_display = 'N/A'
    fieldsets = (
        ("基本信息", {"fields": ("title", "cover", "music", "cat", "tags",)}),
        ("标记信息", {"fields": (("is_active", "apply_active"), ("is_top", "apply_top"), ("is_fine", "apply_fine"))}),
        ("正文部分", {"fields": ("source", "content",)}),
        ("统计信息", {"fields": (("read", "like"), "mod", "add",)}),
    )

    def save_model(self, request, obj, form, change):
        # todo 新增文章时, 发邮件给站长, 提示站长进行审核
        # if not change: send_mail
        # 当没有作者时, 将当前登陆者作为作者
        if (not hasattr(obj, 'author')) or (not obj.author):
            obj.author = request.user
        obj.save()

    def get_queryset(self, request):
        # 筛选出当前登陆者的文章
        qs = super().get_queryset(request)
        return qs.filter(author_id=request.user.id)

    def has_add_permission(self, request):
        # 写文章的权限
        if request.user.is_superuser:
            return True
        return request.user.is_active

    def has_delete_permission(self, request, obj=None):
        # 删除权限
        if obj is not None:
            if request.user.is_superuser:
                return True
            if request.user.id == obj.author.id:
                return True
        return False

    # def has_change_permission(self, request, obj=None):
    # todo: 此处只要重写就会引发403, 原因暂时不明
    # super().has_change_permission(request, obj)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', "published", "to_publish", "read", "like")
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login', 'email', 'is_active', 'is_staff', 'is_superuser',
                       "published", "to_publish", "read", "like")
    exclude = ('last_name', 'first_name', 'groups', 'user_permissions', "password")
    style_fields = {'user_permissions': 'm2m_transfer'}
    fieldsets = (
        ("基本信息", {"fields": ("email", "username", "header", "desc", "alipay", "wechat")}),
        ("账户状态", {"fields": ("is_active", "is_staff", "is_superuser",)}),
        ("统计信息", {"fields": ("date_joined", "last_login", "published", "to_publish", "read", "like")}),
    )

    def get_queryset(self, request):
        # 筛选自己的账号
        qs = super().get_queryset(request)
        return qs.filter(id=request.user.id)

    def save_model(self, request, obj, form, change):
        if not obj.email:
            obj.email = 'author@lujianxin.com'
        obj.save()

    # def has_change_permission(self, request, obj=None):
    #     if obj is not None:
    #         if request.user.id == obj.id:
    #             return True

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'is_active', "published", "to_publish", "read", "like")
    ordering = ('-date_joined',)
    list_per_page = 60
    list_editable = ("is_active",)
    search_fields = ('username', 'email')
    readonly_fields = ('date_joined', 'last_login', "published", "to_publish", "read", "like")
    exclude = ('last_name', 'first_name',)
    style_fields = {'user_permissions': 'm2m_transfer'}
    fieldsets = (
        ("基本信息", {"fields": ("email", "username", "header", "desc", "alipay", "wechat")}),
        ("权限信息", {"fields": ('groups', 'user_permissions')}),
        ("账户状态", {"fields": ("is_active", "is_staff", "is_superuser",)}),
        ("统计信息", {"fields": ("date_joined", "last_login", "published", "to_publish", "read", "like")}),
    )

    def save_model(self, request, obj, form, change):
        # todo 新增账户时, 发邮件给对应邮箱, 恭喜注册成功
        # if not change: send_mail
        if not obj.email:
            obj.email = 'author@lujianxin.com'
        obj.save()


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('ad_name', 'adtype', 'url', 'end')
    list_per_page = 60
    list_editable = ("adtype",)
    search_fields = ('ad_name', 'remark')
    list_filter = ("adtype",)
    readonly_fields = ('add', 'mod')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('link_name', 'is_active', 'cat', 'url')
    search_fields = ('link_name', 'email', 'link')
    list_editable = ("is_active", "cat")
    list_per_page = 60
    list_filter = ("cat", 'is_active')
    readonly_fields = ('add', 'mod')


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'add', 'url')
    search_fields = ('title',)
    list_filter = ('is_active',)
    list_per_page = 60
    list_editable = ("is_active",)
    readonly_fields = ('add', 'mod')


class ExpandAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', "mod")
    search_fields = ('remark', 'key')
    list_per_page = 60
    ordering = ('-mod',)
    readonly_fields = ('mod',)


admin.site.register(Music, MusicAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(AuthorBlog, AuthorBlogAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Expand, ExpandAdmin)
