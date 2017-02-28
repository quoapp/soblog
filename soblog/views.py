
from django.shortcuts import render,render_to_response
#Create your views here.
from soblog.models import *
from soblog.forms import *
from blogspider.blogspider import get_item_info
from django.http import Http404,HttpResponseRedirect
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm


def Register(request):
    if request.method == "POST":
        uf = UserCreationForm(request.POST)
        if uf.is_valid():
            user = uf.save(commit=False)
            user.save()
            return render_to_response('submit_success.html',{})
    else:
        uf = UserCreationForm()
    return render(request,'register.html',{'uf':uf})


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
    get_item_info('python', 1, 20) # 可行，但要放到后台。读取出来内容为html格式，template需要调整
    blogs = Blog.objects.all().order_by('-create_time')
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


@login_required
def user_profile_view(request):
    if request.method == 'POST':
        form_type = request.POST.get('form_type',None)
        if form_type == 'password':
            user_form = MyPasswordChangeForm(request.user, request.POST )
            if user_form.is_valid():
                user_form.save()
                return HttpResponseRedirect(reverse('user_profile'))
            else:
                user_profile = UserProfile.object.filter(user=request.user).first()
                profile_form = UserProfileForm(instance=user_profile)
        elif form_type == 'avatar':
            user_profile = UserProfile.objects.get_or_create(user=request.user)[0]
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if profile_form.is_valid():
                profile_form.save()
                return HttpResponseRedirect(reverse('user_profile'))
            else:
                user_form = MyPasswordChangeForm(request.user)
    else:
        user_profile = UserProfile.objects.filter(user=request.user)
        profile_form = UserProfileForm()
        user_form = MyPasswordChangeForm(request.user)

    return render(
        request,
        'userprofile.html',
        {
            'user_form':user_form,
            'profile_form':profile_form,
        }
    )