# coding: utf-8
from django.db import models
from ljx import settings
from DjangoUeditor.models import UEditorField
from lxml import etree

from db import NewUUID

short_uuid = NewUUID()


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


class Category(models.Model):
    """
    分类
    """
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


class Visitor(models.Model):
    """
    访客表: 电子邮箱作为唯一访客标识, 访客如需留言评论, 必须以电子邮件作为账户登录
    """
    id = models.EmailField(max_length=32, primary_key=True, verbose_name='邮箱', help_text='最多32字符')
    nickname = models.CharField(max_length=12, verbose_name='昵称', unique=True, help_text='1~12个字')
    header = models.ImageField(null=True, blank=True, verbose_name='头像', upload_to='header/')
    pwd = models.CharField(max_length=20, blank=True, null=True, verbose_name='密码')
    desc = models.TextField(max_length=200, blank=True, verbose_name='简介', null=True, help_text='200字描述一下自己')
    is_author = models.BooleanField(default=True, verbose_name='是否作者')
    alipay = models.ImageField(upload_to='dsm/alipay/', null=True, verbose_name='支付宝打赏码', blank=True)
    wechat = models.ImageField(upload_to='dsm/wechat/', null=True, verbose_name='微信打赏码', blank=True)
    is_active = models.BooleanField(default=False, verbose_name='是否可用')
    mod = models.DateTimeField(auto_now=True, verbose_name='最近修改')
    add = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    class Meta:
        verbose_name_plural = verbose_name = '访客'
        db_table = 'visitor'

    def __str__(self):
        return self.nickname

    def origin(self):
        # 原创文章数
        ocnt = Blog.objects.filter(
            is_active=True,
            author__id=self.id,
            source__isnull=True
        ).count()
        return ocnt

    def copy(self):
        # 转载文章数
        ccnt = Blog.objects.filter(
            is_active=True,
            author__id=self.id,
            source__isnull=False
        ).count()
        return ccnt

    def join(self):
        # 加入本站天数
        import datetime
        now = datetime.datetime.now()
        t = now - self.add
        return t.days


class Blog(models.Model):
    """
    博客: 分类控制: 顶部3-4张轮播图, 右侧2小窗口
    """
    id = models.CharField(max_length=12, default=short_uuid.random, primary_key=True)
    title = models.CharField(max_length=32, verbose_name='标题', help_text='1~32个字')
    author = models.ForeignKey(to=Visitor, on_delete=models.CASCADE, verbose_name='作者')
    cat = models.ForeignKey(to=Category, related_name='cblogs', on_delete=models.SET_NULL, null=True, verbose_name='分类')
    tags = models.ManyToManyField(to=Tag, related_name='tblogs', verbose_name='标签', blank=True)
    cover = models.ImageField(upload_to='blog/cover/', verbose_name='封面', blank=True)
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
    is_active = models.BooleanField(default=True, verbose_name='是否可用')

    class Meta:
        verbose_name_plural = verbose_name = '博客'
        db_table = 'blog'

    def __str__(self):
        return self.title

    def url(self):
        # 前台展示链接
        from django.utils.safestring import mark_safe
        full_path = '{}/art/{}'.format(settings.SERVER, self.pk)
        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(full_path, full_path))

    url.short_description = '前去阅读'

    def com(self):
        coms = self.coms.filter(is_active=True)
        # 评论条数
        com_cnt = coms.count()
        return com_cnt

    com.short_description = '评论数'

    def original(self):
        # 是否原创: 有source链接则为转载, 否则为原创
        if self.source:
            from django.utils.safestring import mark_safe
            return mark_safe('<a href="{}" target="_blank">转载</a>'.format(self.source))
        return '原创'

    original.short_description = '创作类型'

    def description(self):
        # 返回文章的非富文本字符串
        e = etree.HTML(self.content)
        text = e.xpath('string(.)').strip()
        return text[:settings.ART_DESC_LENGTH]

    def keywords(self):
        # 用于文章详情页seo优化的关键字
        tags = self.tags.filter(is_active=True)
        return '、'.join([tag.tag for tag in tags])

    def act_coms(self):
        # 文章对应的可见评论
        return self.coms.filter(is_active=True)


class TopBlog(Blog):
    """
    置顶博客： 轮播图级旁边两个小窗
    """

    class Meta:
        verbose_name_plural = verbose_name = '置顶博客'
        proxy = True


class Comment(models.Model):
    """
    评论表, 简单的1问1答模式，如果是游客，visitor字段不为空，否则email字段不为空
    """
    blog = models.ForeignKey(to=Blog, related_name='coms', on_delete=models.CASCADE, verbose_name='所属博客')
    visitor = models.ForeignKey(to=Visitor, on_delete=models.CASCADE, null=True, blank=True, verbose_name='评论者')
    nickname = models.CharField(max_length=12, null=True, blank=True, verbose_name='昵称')
    email = models.EmailField(max_length=64, verbose_name='邮箱', null=True, blank=True)
    content = UEditorField(verbose_name='评论内容', max_length=300, width='100%', height=200, blank=True,
                           imagePath='com/v/',
                           toolbars='normal')
    reply = UEditorField(verbose_name='作者回复', max_length=300, width='100%', height=200, blank=True, imagePath='com/r/',
                         toolbars='normal')
    add = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')
    rep = models.DateTimeField(default=None, null=True, blank=True, verbose_name='回复时间')
    is_active = models.BooleanField(default=False, verbose_name='是否可用')

    class Meta:
        verbose_name_plural = verbose_name = '评论'
        db_table = 'comment'

    def __str__(self):
        e = etree.HTML(self.content)
        text = e.xpath('string(.)').strip()
        return text[:settings.COM_DESC_LENGTH] or '-x-'

    def obj_type(self):
        if not self.visitor:
            if self.nickname and self.email:
                return '游客'
            return '未知'
        return '会员'

    obj_type.short_description = '访客类型'


class Message(models.Model):
    """
    留言, 一问一答模式, 没有楼层嵌套, visitor不为空则为已注册会员发言，否则为未注册，依靠nickname和email收信
    """
    visitor = models.ForeignKey(to=Visitor, on_delete=models.CASCADE, verbose_name='访客')
    nickname = models.CharField(max_length=12, null=True, blank=True, verbose_name='昵称')
    email = models.EmailField(max_length=64, verbose_name='邮箱', null=True, blank=True)
    content = UEditorField(verbose_name='内容', max_length=300, width='100%', blank=True, imagePath='msg/v/',
                           toolbars='normal')
    reply = UEditorField(max_length=300, null=True, verbose_name='站长回复', blank=True, width='100%',
                         imagePath='msg/r/', toolbars='normal')
    add = models.DateTimeField(auto_now_add=True, verbose_name='留言时间')
    rep = models.DateTimeField(default=None, null=True, blank=True, verbose_name='回复时间')
    is_active = models.BooleanField(default=False, verbose_name='是否可见')

    class Meta:
        verbose_name_plural = verbose_name = '留言'
        db_table = 'message'

    def __str__(self):
        e = etree.HTML(self.content)
        text = e.xpath('string(.)').strip()
        return text[:settings.MSG_DESC_LENGTH] or '-x-'

    def obj_type(self):
        if not self.visitor:
            if self.email and self.nickname:
                return '游客'
            return '未知'
        return '会员'

    obj_type.short_description = '访客类型'


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
        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(self.link, self.link))

    url.short_description = '广告链接'


class TipAd(Advertisement):
    """
    左侧长条广告
    """

    class Meta:
        verbose_name_plural = verbose_name = '长条广告'
        proxy = True


class AdClick(models.Model):
    """
    广告点击记录
    """
    advertisement = models.ForeignKey(to=Advertisement, on_delete=models.CASCADE, verbose_name='广告')
    ip = models.GenericIPAddressField(default='0.0.0.0', verbose_name='IP地址')
    user_agent = models.TextField(default=settings.DEFAULT_UA, max_length=128, verbose_name='设备信息')
    add = models.DateTimeField(auto_now_add=True, verbose_name='点击时间')

    class Meta:
        verbose_name_plural = verbose_name = '广告点击统计'
        db_table = 'adclick'

    def __str__(self):
        return self.advertisement.ad_name


class Link(models.Model):
    """
    友情链接: 需要分类
    """
    cats = (
        (0, '公益链接'),
        (1, '个人主页'),
        (2, '商业广告'),
    )
    link = models.URLField(max_length=64, verbose_name='链接', primary_key=True)
    link_name = models.CharField(max_length=32, verbose_name='链接名称')
    cat = models.PositiveSmallIntegerField(choices=cats, default=0, verbose_name='链接类型')
    email = models.EmailField(max_length=32, verbose_name='邮箱')
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
        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(self.link, self.link))

    url.short_description = '跳转链接'


class Click(models.Model):
    """
    从我网站点击友链的统计, 每月推送给对方
    """
    link = models.ForeignKey(to=Link, on_delete=models.CASCADE, verbose_name='链接')
    ip = models.GenericIPAddressField(default='0.0.0.0', verbose_name='IP地址')
    user_agent = models.CharField(default=settings.DEFAULT_UA, max_length=128, verbose_name='设备信息')
    add = models.DateTimeField(auto_now_add=True, verbose_name='点击时间')

    class Meta:
        verbose_name_plural = verbose_name = '友链点击统计'
        db_table = 'click'

    def __str__(self):
        return self.ip


class Focus(models.Model):
    """
    邮箱订阅: 每周末推送上一周的新文章
    """
    id = models.EmailField(max_length=32, primary_key=True, verbose_name='邮箱')
    add = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    mod = models.DateTimeField(auto_now=True, verbose_name='最近修改')
    is_active = models.BooleanField(default=True, verbose_name='是否接收')

    class Meta:
        verbose_name_plural = verbose_name = '订阅'
        db_table = 'focus'

    def __str__(self):
        return self.pk


class Email(models.Model):
    """
    邮件发送记录:
    友链: 每月发送一次, 正文写有多少条记录来自于我这, 推荐几篇最近的文章, 附件部分发送生成的表格详细记录
    """
    cats = (
        (0, '订阅推送'),  # 每周一次, 内容相同
        (1, '友链推送'),  # 每月一次, 内容不同
    )
    cat = models.PositiveSmallIntegerField(choices=cats, verbose_name='推送类型')
    total = models.PositiveIntegerField(verbose_name='发送条数', default=0)
    success = models.PositiveIntegerField(verbose_name='成功条数', default=0)
    start = models.DateTimeField(auto_now_add=True, verbose_name='开始时间')
    end = models.DateTimeField(null=True, verbose_name='结束时间')

    class Meta:
        verbose_name_plural = verbose_name = '邮件记录'
        db_table = 'email'

    def __str__(self):
        return '%s-%s' % (self.start, self.end)


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
        full_path = '{}/notice/{}'.format(settings.SERVER, self.pk)
        return mark_safe('<a href="{}" target="_blank">{}</a>'.format(full_path, full_path))

    url.short_description = '公告链接'


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
