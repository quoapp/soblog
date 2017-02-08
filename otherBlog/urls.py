"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
#coding:utf-8

from django.conf.urls import url
from django.contrib import admin
from soblog.views import *
admin.autodiscover()

urlpatterns = [
    url(r'^admin/',admin.site.urls),
    url(r'^blogs/$',get_blogs,name="blog_list"),
    url(r'^detail/(\d+)/$',get_details,name='blog_get_detail'),
    url(r'^blog_login/$',blog_login,name='django.contrib.auth.views.login'),
    url(r'^$', get_blogs,name="blog_list"),
    # url(r'^register/$',Register,name='register'),
    url(r'^blog_post/$',Post_blog,name='blog_post'),
    url(r'^blog/(\d+)/edit/$',Blog_edit,name='blog_edit')
    # url(r'^submit_success/$',name='submit_success') #缺view值
]
