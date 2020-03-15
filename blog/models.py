# coding: utf-8
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from ishare import settings
from DjangoUeditor.models import UEditorField
from lxml import etree

from blog import NewUUID

short_uuid = NewUUID()


class Music(models.Model):
    """
    文章详情页的bgm
    """
    name = models.CharField(max_length=64, verbose_name='音乐名')
    author = models.CharField(max_length=20, verbose_name='歌手')
    code = models.TextField(max_length=300, verbose_name='外链代码')
    mod = models.DateTimeField(auto_now=True, verbose_name='最后变更')
    is_active = models.BooleanField(default=True, verbose_name='是否可用')

    class Meta:
        verbose_name_plural = verbose_name = '外链音乐'
        db_table = 'music'
        unique_together = (('name', 'author'),)

    def __str__(self):
        return '{}-{}'.format(self.author, self.name)

    def art_nums(self):
        """此音乐被多少文章使用"""
        return self.mblogs.all().count()

    art_nums.short_description = '引用次数'


class Tag(models.Model):
    """
    标签
    """
    tag = models.CharField(max_length=12, verbose_name='标签', unique=True, help_text='1~12个字')
    add = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    mod = models.DateTimeField(auto_now=True, verbose_name='最近修改')
    is_active = models.BooleanField(default=True, verbose_name='是否可用')

    class Meta:
        verbose_name_plural = verbose_name = '标签'
        db_table = 'tag'

    def __str__(self):
        return self.tag

    def art_nums(self):
        return self.tblogs.all().count()

    art_nums.short_description = '文章数'

    def url(self):
        # 前台展示链接
        from django.utils.safestring import mark_safe
        if self.is_active:
            full_path = '{}/x/tag/{}/'.format(settings.SERVER, self.pk)
            return mark_safe('<a href="{}" target="_blank">{}</a>'.format(full_path, full_path))
        return "不可用标签"

    url.short_description = '前去阅读'

    def get_absolute_url(self):
        return '/x/tag/{}/'.format(self.pk)


class Category(models.Model):
    """
    分类
    """
    pre_cats = (
        ('A', '文学类'),
        ('B', '技术类'),
    )
    pre_cat = models.CharField(max_length=1, choices=pre_cats, verbose_name='前置分类')
    cat = models.CharField(max_length=12, verbose_name='类别', help_text='1~12个字')
    add = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    mod = models.DateTimeField(auto_now=True, verbose_name='最近修改')
    is_active = models.BooleanField(default=True, verbose_name='是否可用')

    class Meta:
        verbose_name_plural = verbose_name = '类别'
        db_table = 'category'

    def __str__(self):
        return self.cat

    def art_nums(self):
        return self.cblogs.count()

    art_nums.short_description = '文章数'

    def url(self):
        # 前台展示链接
        from django.utils.safestring import mark_safe
        if self.is_active:
            full_path = '{}/x/cat/{}'.format(settings.SERVER, self.pk)
            return mark_safe('<a href="{}" target="_blank">{}</a>'.format(full_path, full_path))
        return "不可用分类"

    url.short_description = '前去阅读'

    def get_absolute_url(self):
        return '/x/cat/{}/'.format(self.pk)


class UserAccount(AbstractUser):
    """
    重构user模型,适应作者需求， username 为作者昵称
    """
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        help_text='作者昵称、2~30个字符',
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        verbose_name='账号邮箱',
        unique=True,
        help_text='作为登录账号，绑定后不可修改'
    )
    header = models.ImageField(null=True, blank=True, verbose_name='头像', upload_to='header/')
    desc = models.TextField(max_length=200, blank=True, verbose_name='简介', null=True, help_text='200字描述一下自己')
    alipay = models.ImageField(upload_to='dsm/alipay/', null=True, verbose_name='支付宝打赏码', blank=True)
    wechat = models.ImageField(upload_to='dsm/wechat/', null=True, verbose_name='微信打赏码', blank=True)

    class Meta:
        verbose_name_plural = verbose_name = '账户'
        db_table = 'user_account'

    def __str__(self):
        return self.username

    def origin(self):
        # 原创文章数
        ocnt = Blog.objects.filter(
            is_active=True,
            author=self.pk,
            source__isnull=True
        ).count()
        return ocnt

    def copy(self):
        # 转载文章数
        ccnt = Blog.objects.filter(
            is_active=True,
            author=self.pk,
            source__isnull=False
        ).count()
        return ccnt

    def join(self):
        # 加入本站天数
        import datetime
        now = datetime.datetime.now()
        t = now - self.date_joined
        return t.days

    def published(self):
        # 作者在本站已发表文章数
        return Blog.objects.filter(author_id=self.id, is_active=True, cat__is_active=True).count()

    published.short_description = "累计发表文章"

    def to_publish(self):
        return Blog.objects.filter(Q(is_active=False) | Q(cat__is_active=False), author_id=self.id).count()

    to_publish.short_description = "暂未发表文章"

    def read(self):
        # 总阅读量
        bs = Blog.objects.only("read").filter(author_id=self.id)
        return sum([b.read for b in bs])

    read.short_description = "阅读量"

    def like(self):
        bs = Blog.objects.only("like").filter(author_id=self.id)
        return sum([b.like for b in bs])

    like.short_description = "点赞量"


class Author(UserAccount):
    class Meta:
        verbose_name_plural = verbose_name = '账户中心'
        proxy = True


class Blog(models.Model):
    """
    博客: 分类控制: 顶部3-4张轮播图, 右侧2小窗口
    """
    id = models.CharField(max_length=12, default=short_uuid.random, primary_key=True)
    title = models.CharField(max_length=32, verbose_name='标题', help_text='1~32个字')
    author = models.ForeignKey(
        to=UserAccount,
        on_delete=models.CASCADE,
        limit_choices_to={
            "is_active": True,
            "is_staff": True,
        },
        verbose_name='作者'
    )
    cat = models.ForeignKey(to=Category, related_name='cblogs', limit_choices_to={'is_active': True},
                            on_delete=models.SET_NULL, null=True, verbose_name='分类')
    tags = models.ManyToManyField(to=Tag, related_name='tblogs', limit_choices_to={'is_active': True},
                                  verbose_name='标签', blank=True)
    cover = models.ImageField(upload_to='blog/cover/', verbose_name='封面', blank=True)
    music = models.ForeignKey(to=Music, on_delete=models.SET_NULL, limit_choices_to={'is_active': True}, null=True,
                              blank=True, verbose_name='背景音乐', related_name='mblogs')
    # mini, normal, full, besttome, 四种工具栏, normal比较适合留言, 评论
    content = UEditorField(verbose_name='内容', width='100%', blank=True, imagePath='blog/img/', toolbars='full',
                           filePath='blog/file/')
    source = models.URLField(null=True, blank=True, verbose_name='原文链接', help_text='如果转载, 则提供原文链接')
    is_fine = models.BooleanField(default=False, verbose_name='站长推荐')
    is_top = models.BooleanField(default=False, verbose_name='是否置顶')
    read = models.PositiveIntegerField(default=0, verbose_name='阅读数')
    like = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    add = models.DateTimeField(auto_now_add=True, verbose_name='发表时间')
    mod = models.DateTimeField(auto_now=True, verbose_name='最后修改')
    is_active = models.BooleanField(default=False, verbose_name='是否可用')

    class Meta:
        verbose_name_plural = verbose_name = '文章'
        db_table = 'blog'

    def __str__(self):
        return self.title

    def url(self):
        # 前台展示链接
        from django.utils.safestring import mark_safe
        if self.is_active and self.cat.is_active:
            full_path = '{}/x/art/{}'.format(settings.SERVER, self.pk)
            return mark_safe('<a href="{}" target="_blank">{}</a>'.format(full_path, full_path))
        return "不可见文章"

    url.short_description = '前去阅读'

    def original(self):
        # 是否原创: 有source链接则为转载, 否则为原创
        if self.source:
            from django.utils.safestring import mark_safe
            return mark_safe('<a href="{}" target="_blank">转载</a>'.format(self.source))
        return '原创'

    original.short_description = '创作类型'

    def description(self):
        # 返回文章的非富文本字符串
        e = etree.HTML(self.content or "本文暂无内容")
        text = e.xpath('string(.)').strip()
        obj = Expand.objects.filter(key="ART_DESC_LENGTH").first()
        num = int(obj.value) if obj else settings.ART_DESC_LENGTH
        return text[:num]

    def keywords(self):
        # 用于文章详情页seo优化的关键字
        tags = self.tags.filter(is_active=True)
        return '、'.join([tag.tag for tag in tags])

    def get_absolute_url(self):
        return '/x/art/{pk}'.format(pk=self.pk)


class AuthorBlog(Blog):
    """
    给作者用的博客管理器
    """

    class Meta:
        verbose_name_plural = verbose_name = '我的文章'
        proxy = True

    def apply_top(self):
        return "功能即将上线^c^"

    apply_top.short_description = "申请置顶"

    def apply_active(self):
        return "功能即将上线^c^"

    apply_active.short_description = "提交审核"

    def apply_fine(self):
        return "功能即将上线^c^"

    apply_fine.short_description = "申请推荐"


class Advertisement(models.Model):
    """
    广告位: 右侧部分图片元素
    """
    adtypes = (
        (0, '右侧方形广告'),
        (1, '左侧长条广告'),
    )
    ad_name = models.CharField(max_length=20, verbose_name='广告名')
    image = models.ImageField(upload_to='ad/', verbose_name='图片', blank=True)
    link = models.URLField(verbose_name='广告链接')
    adtype = models.PositiveSmallIntegerField(choices=adtypes, null=True, blank=True, verbose_name='广告类型')
    remark = models.TextField(max_length=64, verbose_name='备注', null=True, blank=True)
    add = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    mod = models.DateTimeField(auto_now=True, verbose_name='最近修改')
    end = models.DateTimeField(null=True, verbose_name='结束时间')

    class Meta:
        verbose_name_plural = verbose_name = '广告'
        db_table = 'advertisement'

    def __str__(self):
        return self.ad_name

    def url(self):
        # 跳转链接
        from django.utils.safestring import mark_safe
        return mark_safe(
            '<a href="{}?from={}" target="_blank">{}</a>'.format(self.link, settings.ALLOWED_HOSTS[0], self.link))

    url.short_description = '广告链接'


class Link(models.Model):
    """
    友情链接: 需要分类
    """
    cats = (
        (0, '公益链接'),
        (1, '个人主页'),
        (2, '商业广告'),
    )
    link = models.URLField(max_length=64, verbose_name='链接', unique=True, help_text='完整的网站首页地址')
    link_name = models.CharField(max_length=32, verbose_name='链接名称', help_text='网站的名字')
    cat = models.PositiveSmallIntegerField(choices=cats, default=1, verbose_name='链接类型', help_text='网站类型')
    email = models.EmailField(max_length=32, verbose_name='邮箱', help_text='有特殊情况方便联系')
    add = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    mod = models.DateTimeField(auto_now=True, verbose_name='最近修改')
    is_active = models.BooleanField(default=False, verbose_name='是否可用')

    class Meta:
        verbose_name_plural = verbose_name = '友链'
        db_table = 'link'

    def __str__(self):
        return self.link_name

    def url(self):
        # 跳转链接
        from django.utils.safestring import mark_safe
        return mark_safe(
            '<a href="{}?from={}" target="_blank">{}</a>'.format(self.link, settings.ALLOWED_HOSTS[0], self.link))

    url.short_description = '跳转链接'


class Notice(models.Model):
    """
    公告: 首页右侧展示三条
    """
    title = models.CharField(max_length=20, verbose_name='标题', help_text='1~20个字')
    content = UEditorField(verbose_name='详情', width='100%', blank=True, imagePath='notice/img/', toolbars='full',
                           filePath='notice/file/')
    add = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    mod = models.DateTimeField(auto_now=True, verbose_name='最近修改')
    is_active = models.BooleanField(default=True, verbose_name='是否可见')

    class Meta:
        verbose_name_plural = verbose_name = '公告'
        db_table = 'notice'

    def __str__(self):
        return self.title

    def url(self):
        # 前台展示链接
        from django.utils.safestring import mark_safe
        full_path = '{}/x/notice/{}'.format(settings.SERVER, self.pk)
        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(full_path, full_path))

    url.short_description = '公告链接'

    def keywords(self):
        return self.title

    def description(self):
        return self.title


class Expand(models.Model):
    """
    仅用于键值格式, 用于存储网站的一些信息
    """
    key = models.CharField(max_length=16, verbose_name='键', primary_key=True, help_text='1~16字符')
    value = models.CharField(max_length=32, verbose_name='值', help_text='1~32字符')
    remark = models.TextField(max_length=100, verbose_name='备注', null=True)
    mod = models.DateTimeField(auto_now=True, verbose_name='上次变更')

    class Meta:
        verbose_name_plural = verbose_name = '拓展数据'
        db_table = 'expand'

    def __str__(self):
        return self.pk
