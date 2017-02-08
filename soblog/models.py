#coding:utf8
from django.db import models
import datetime
from django.contrib.auth.models import User


class Catagory(models.Model):
    name = models.CharField(max_length = 30,verbose_name="分类")
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=16,verbose_name="标签")
    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(verbose_name='标题',max_length=150)
    author = models.ForeignKey(User,verbose_name='作者',default='adma')
    # abstract = models.TextField('blog_abstract',blank=True, null=True,max_length=150)
    content = models.TextField(verbose_name='内容',max_length=5000)
    created = models.DateTimeField(verbose_name='发布日期',default=datetime.datetime.now)
    catagory = models.ForeignKey(Catagory,related_name="blog_catagory",verbose_name="分类")
    tags = models.ManyToManyField(Tag,related_name="blog_tag",verbose_name="标签")
    # bloger = models.ForeignKey(Userinfo,blank=True, null=True)
    # view_count = models.IntegerField('view_count',blank=True, null=True,default=0)
    def __str__(self):
        return self.title


class Comment(models.Model):

    blog = models.ForeignKey(Blog,verbose_name='文章')
    name = models.ForeignKey(User,verbose_name='评论人',null=True)
    content = models.TextField(verbose_name='评论内容',max_length=240)
    created = models.DateTimeField(verbose_name='评论时间',default=datetime.datetime.now)

    def __str__(self):
        return self.content


