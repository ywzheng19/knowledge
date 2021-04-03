from django.contrib.auth.models import User
from django.db import models

# 定义分类模型
class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '分类'

    # 定义类方法(类方法可通过类名调用), 获取is_nav=True的正常状态的分类对象
    @classmethod
    def get_navs(cls):
        # 获取正常状态的分类对象
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        # 定义列表, 存储
        nav_categories = []
        for cate in categories:
            if cate.is_nav:
                nav_categories.append(cate)
        return {'navs': nav_categories}
        

    def __str__(self):
        return self.name

# 定义标签模型
class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    
    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name

# 定义知识模型
class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True,  verbose_name="描述")  # blank=True允许字段为空
    content = models.TextField(verbose_name="正文", help_text="正文必须为MarkDown格式")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name="状态")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name="分类")
    tag = models.ManyToManyField(Tag, verbose_name="标签") # 20210223, 修改为多对多, 会生成一个中间表描述多对多关系
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="作者")
    pv = models.PositiveIntegerField(default=0, verbose_name='访问量')  # 20210223增加字段, 统计阅读量
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now_add=True, verbose_name="修改时间")
    is_top = models.BooleanField(default=False, verbose_name="置顶")    # 20210308增加字段, 是否置顶


    class Meta:
        verbose_name = verbose_name_plural = '知识'
        ordering = ['-id']

    def __str__(self):
        return self.title

    # 20210223增加类方法, 获取最新十条知识
    @classmethod
    def ten_latest(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)[:10]  # 返回列表

    # 20210223增加类方法, 获取最热十条知识, 根据阅读量
    @classmethod
    def ten_hotest(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')[:10]   # 返回列表

    # 20210308增加类方法, 获取置顶文章
    @classmethod
    def get_topped(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL, is_top=True)


# 20210314 新增日志模型
class Log(models.Model):
    title = models.DateField(verbose_name="标题")
    content = models.TextField(verbose_name="更新内容")

    class Meta:
        verbose_name = verbose_name_plural = "更新日志"
        ordering = ['-title']

    def __str__(self):
        return str(self.title)

