from django.contrib.auth.models import User
from django.db import models
from django.template.loader import render_to_string

# 定义侧边栏模型
class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEMS = (
        (STATUS_SHOW, '展示'),
        (STATUS_HIDE, '隐藏'),
    )
    DISPLAY_HTML = 1
    DISPLAY_HOTEST = 2
    DISPLAY_LATEST = 3
    SIDE_TYPE = (
        (1, 'HTML'),
        (2, '最热知识'),
        (3, '最新知识'),
    )

    title = models.CharField(max_length=50, verbose_name="标题")
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE, verbose_name="展示类型")
    content = models.CharField(max_length=500, blank=True, verbose_name="内容", help_text="如果不是HTML类型, 可为空")   # blank=True允许字段为空
    status = models.PositiveIntegerField(default=STATUS_SHOW, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "侧边栏"

    def __str__(self):
        return self.title

    # 定义类方法, 返回展示状态的侧边栏对象
    @classmethod
    def get_all(cls):
        sidebars = cls.objects.filter(status=cls.STATUS_SHOW)
        return {'sidebars': sidebars}

    # 定义类属性, 根据不同的展示状态返回不同的内容
    @property
    def content_html(self):
        # 直接渲染模板
        from detail.models import Post
        response = ''
        # 如果展示类型为html, 返回content字段; 如果为最热, 返回最热十条知识; 如果为最新, 返回最新十条知识;
        # 调用Post模型类中定义的类方法
        if self.display_type == self.DISPLAY_HTML:
            response = self.content
        elif self.display_type == self.DISPLAY_HOTEST:
            context = {'posts': Post.ten_hotest}
            response = render_to_string('config/blocks/sidebar_posts.html', context)
        elif self.display_type == self.DISPLAY_LATEST:
            context = {'posts': Post.ten_latest}
            response = render_to_string('config/blocks/sidebar_posts.html', context)
        return response


# 定义友链模型
class Link(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
 
    title = models.CharField(max_length=50, verbose_name="标题")
    href = models.URLField(verbose_name="链接") # 默认长度为200
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1, 6), range(1, 6)), verbose_name="权重", help_text="权重高展示顺序靠前")
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = "友链"

    def __str__(self):
        return self.title
