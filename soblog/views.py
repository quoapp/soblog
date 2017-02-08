from django.shortcuts import render,render_to_response
#Create your views here.
from soblog.models import *
from soblog.forms import *
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
#
# def Register(request):
#     if request.method == "POST":
#         uf = UserForm(request.POST)
#         if uf.is_valid():
#             #获取新的注册信息表单
#             username = uf.cleaned_data['username']
#             password = uf.cleaned_data['password']
#             email = uf.cleaned_data['email']
#             #将表单写入数据库
#             user = Userinfo()
#             user.username = username
#             user.password = password
#             user.email = email
#             user.save()
#             return render_to_response('submit_success.html',{})
#     else:
#         uf = UserForm()
#     return render(request,'register.html',{'uf':uf})


def blog_login(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        user = auth.authenticate(username=username,password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/blogs/")
        else:
            return HttpResponseRedirect("/account/invalid/")
    else:
        form = AuthenticationForm()
        return render(request,'blog_login.html',{'form':form})


def get_blogs(request):
    blogs = Blog.objects.all().order_by('-created')
    return render_to_response('blog_list.html',{'blogs':blogs})


def get_details(request,blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        raise Http404

    if request.method == 'GET':
        form = CommentForm()

    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            cleaned_data['blog'] = blog
            Comment.objects.create(**cleaned_data)

    ctx = {
        'blog':blog,
        'comments':blog.comment_set.all().order_by('-created'),
        'form':form
    }
    return render(request,'blog_details.html',ctx)


@login_required
def Post_blog(request):
    if request.method == "POST":
        bf = BlogForm(request.POST)

        if bf.is_valid():
            post = bf.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_get_detail',post.id)
    else:
        bf = BlogForm()
    return render(request,'blog_post.html',{'bf':bf })


@login_required
def Blog_edit(request,blog_id):
    edit = Blog.objects.get(id=blog_id)

    if request.method == "POST":
        bf = BlogForm(request.POST)
        if bf.is_valid():
            post = bf.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog_get_detail', post.id)
    else:
        bf = BlogForm(instance=edit)
    return render(request,'blog_edit.html',{"bf":bf})
