#coding:utf8
from __future__ import unicode_literals
from django.db import models
import datetime

class Catagory(models.Model):
    # id = models.AutoField('id', primary_key=True)
    name = models.CharField(max_length = 30,verbose_name="分类")
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=16,verbose_name="标签")
    def __str__(self):
        return self.name

class Userinfo(models.Model):
    username = models.CharField(max_length=16,verbose_name="用户名")
    password = models.CharField(max_length=16,verbose_name="密码")
    email = models.EmailField(verbose_name="账户邮箱")
    # phone
    # sex = models.CharField('sex',choices=(("M","Male"),("F","Female")),max_length=7,blank=True, null=True,)
    #qq
    #wechat
    #weibo
    #address
    #birthday
    #image_url
    #job
    #height
    #weight
    #mariage
    #education
    #description
    #blood_type
    #register_time
    # last_login_ip = models.GenericIPAddressField('last_login_ip',blank=True, null=True,)
    # last_login_date = models.DateTimeField('last_login_date)',blank=True, null=True,)
    #rank
    #record
    def __str__(self):
        return self.username

class Blog(models.Model):
    title = models.CharField(verbose_name='标题',max_length=150)
    author = models.CharField(verbose_name='作者',max_length=16,blank=True, null=True,default='adma')
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
    name = models.CharField(verbose_name='评论人',max_length=16,blank=True, null=True)
    # email = models.EmailField('email')
    content = models.TextField(verbose_name='评论内容',max_length=240)
    created = models.DateTimeField(verbose_name='评论时间',default=datetime.datetime.now)

    def __str__(self):
        return self.content


