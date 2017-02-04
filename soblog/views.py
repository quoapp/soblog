from django.shortcuts import render,render_to_response
#Create your views here.
from soblog.models import *
from soblog.forms import *
from django.http import Http404


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

def Post_blog(request):
    if request.method == "POST":
        bf = BlogForm(request.POST)
        # cf = CatagoryForm(request.POST)
        # tf = TagForm(request.POST)

        if bf.is_valid():
            title = bf.cleaned_data['title']
            author = bf.cleaned_data['author']
            content = bf.cleaned_data['content']
            catagory = bf.cleaned_data['catagory']
            tag_names = bf.cleaned_data['tags']

            blog = Blog()
            blog.title = title
            blog.author = author
            blog.content = content
            blog.catagory = catagory
            # blog.tags = tag_names
            blog.save()
            return render_to_response('submit_success.html',{})
    else:
        bf = BlogForm()
    return render(request,'blog_post.html',{'bf':bf })

def Register(request):
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取新的注册信息表单
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            #将表单写入数据库
            user = Userinfo()
            user.username = username
            user.password = password
            user.email = email
            user.save()
            return render_to_response('submit_success.html',{})
    else:
        uf = UserForm()
    return render(request,'register.html',{'uf':uf})