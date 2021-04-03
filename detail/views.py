import logging
FORMAT = '%(asctime)s-%(name)s-%(funcName)s:%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT)

from functools import wraps

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q, F
from django.contrib import auth
from django.contrib.auth.models import User

from .models import Category, Tag, Post, Log
from config.models import SideBar


# 20210307 增加装饰器, 检查用户是否登录;
# 已登录用户继续调用原函数, 未登录用户跳转登录页面.
def login_decorator(func):
    @wraps(func)
    def login(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'detail/login.html')
    return login

# 20210307 增加登录方法; 登录页面提交用户名密码, 调用此方法;
# auth.authenticate()校验用户名和密码;
# 校验通过执行登录操作并重定向到首页; 校验失败渲染当前页面, 提示用户名或密码错误.
def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)
    logging.debug('username: %s' % username)
    logging.debug('password: %s' % password)
    logging.debug(user)
    if user is not None:
        auth.login(request, user)
        return redirect('/')
    else:
        return render(request, 'detail/login.html', {'message': '用户名或密码错误'})

# 20210308 增加注销方法
def logout(request):
    auth.logout(request)
    return render(request, 'detail/login.html')


@login_decorator
def post_list(request, category_id=None, tag_id=None):
    # 若访问标签列表页, 即传参tag_id, 若tag_id不存在捕获异常返回空知识列表; 防止查不到tag对象报错
    context = {}
    if tag_id:
        try:
            tag = Tag.objects.get(id=tag_id)
            context.update({'tag': tag})
        except Tag.DoesNotExist:
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    else:
        post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
        # 若访问分类列表页, 即传参category_id, 正常状态的知识列表再次根据category_id过滤
        if category_id:
            category = Category.objects.get(id=category_id)
            post_list = post_list.filter(category_id=category_id)
            context.update({'category': category})
    # 20210223 增加分页功能
    page_num = request.GET.get('page', 1)   # 获取请求中page参数值, 未获取到默认为1, GET请求
    page_of_posts, post_list = paginator(page_num, post_list)   # 获取请求分页对应知识列表

    # 20210308 获取置顶知识
    post_top = Post.get_topped()

    # 定义字典, 最后赋予context, 传递给模板
    context.update({'post_list': post_list})
    context.update(Category.get_navs()) # 调用models里定义的类方法get_navs获取可导航的正常分类
    context.update(SideBar.get_all())   # 调用models里定义的类方法get_all获取展示状态的侧边栏
    context.update({'page_obj': page_of_posts})   # 20210223, 增加传递分页对象给模板 
    context.update({'post_top': post_top})  # 20210308, 增加置顶知识对象给模板
    logging.debug(context)
    logging.debug(context.get('post_list'))
    logging.debug(context.get('post_list').count())
    return render(request, 'detail/list.html', context=context)

# 20210303 抽取分页器处理
def paginator(page_num, post_list):
    paginator = Paginator(post_list, 5) # 实例化分页器, (知识列表, 每页5)
    page_of_posts = paginator.get_page(page_num)    # 获取请求分页对象
    post_list = page_of_posts.object_list   # 获取请求分页对应知识列表
    return page_of_posts, post_list # 返回请求分页对象, 对应知识列表

@login_decorator
def post_detail(request, post_id=None):
    # logging.debug(request)
    try:
        post = Post.objects.get(id=post_id)
        if not request.COOKIES.get('post_%s_readed' % post_id): # 判断请求中是否有阅读缓存, 没有则增加阅读次数
            post.pv += 1
            post.save()
    except Post.DoesNotExist:
        post = None
    context = {'post': post}
    context.update(Category.get_navs()) # 20210223, detail页面也需展示分类
    context.update(SideBar.get_all())   # 20210223, detail页面也需展示侧边栏
    # return render(request, 'detail/detail.html', context=context)
    response = render(request, 'detail/detail.html', context=context) # 响应
    response.set_cookie('post_%s_readed' % post_id, 'true', max_age=60) # 用户阅读当前知识详情, 设置阅读缓存, 有效期为1分钟
    return response

# 20210303 增加搜索方法
@login_decorator
def search(request):
    keyword = request.GET.get('keyword', '')
    page_num = request.GET.get('page', 1)
    post_list_normal = Post.objects.filter(status=Post.STATUS_NORMAL)
    if not keyword:
        post_list_keyword = post_list_normal
    post_list_keyword = post_list_normal.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))
    page_of_posts, post_list = paginator(page_num, post_list_keyword)   # 获取请求分页对应知识列表
    
    context = {'post_list': post_list}
    context.update(Category.get_navs()) # 调用models里定义的类方法get_navs获取可导航的正常分类
    context.update(SideBar.get_all())   # 调用models里定义的类方法get_all获取展示状态的侧边栏
    context.update({'page_obj': page_of_posts})   # 20210223, 增加传递分页对象给模板 

    return render(request, 'detail/list.html', context=context)
    


@login_decorator
def author(request, owner_id=None):
    post_list = Post.objects.filter(owner_id=owner_id)
    # 20210223 增加分页功能
    page_num = request.GET.get('page', 1)   # 获取请求中page参数值, 未获取到默认为1, GET请求
    page_of_posts, post_list = paginator(page_num, post_list)   # 获取请求分页对应知识列表

    # 定义字典, 最后赋予context, 传递给模板
    context = {'post_list': post_list}
    context.update(Category.get_navs()) # 调用models里定义的类方法get_navs获取可导航的正常分类
    context.update(SideBar.get_all())   # 调用models里定义的类方法get_all获取展示状态的侧边栏
    context.update({'page_obj': page_of_posts})   # 20210223, 增加传递分页对象给模板 

    return render(request, 'detail/list.html', context=context)

@login_decorator
def changelog(request):
    log_list = Log.objects.all()
    context={'log_list': log_list}
    context.update(Category.get_navs()) # 调用models里定义的类方法get_navs获取可导航的正常分类
    context.update(SideBar.get_all())   # 调用models里定义的类方法get_all获取展示状态的侧边栏
    return render(request, 'detail/changelog.html', context=context)
    
