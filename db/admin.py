from django.contrib import admin
from django.contrib.auth import get_user_model
# Register your models here.
from db.models import (
    Tag,
    Category,
    Blog,
    AuthorBlog,
    Author,
    Advertisement,
    TipAd,
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


class TagAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class BlogAdmin(admin.ModelAdmin):
    pass


class AuthorBlogAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


class AccountAdmin(admin.ModelAdmin):
    pass


class AdvertisementAdmin(admin.ModelAdmin):
    pass


class TipAddAdmin(admin.ModelAdmin):
    pass


class AdClickAdmin(admin.ModelAdmin):
    pass


class LinkAdmin(admin.ModelAdmin):
    pass


class ClickAdmin(admin.ModelAdmin):
    pass


class NoticeAdmin(admin.ModelAdmin):
    pass


class ExpandAdmin(admin.ModelAdmin):
    pass


admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(AuthorBlog, AuthorBlogAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(TipAd, TipAddAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Expand, ExpandAdmin)


