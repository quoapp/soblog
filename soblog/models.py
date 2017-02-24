#coding:utf8
from django.utils.translation import ugettext as _
import datetime
from django.db import models
from django.contrib.auth.models import User
# from imagekit.models import ImageSpecField


STATUS = {
    0:'正常',
    1:'草稿',
    2:'删除',
}


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    token = models.IntegerField(default=0)
    qq = models.CharField(max_length=20,blank=True,null=True,unique=True,verbose_name='QQ号码')
    mobile = models.CharField(max_length=11,blank=True,null=True,unique=True,verbose_name='手机号码')
    wechat = models.CharField(max_length=100,blank=True,null=True,unique=True,verbose_name='微信号')
    avatar = models.ImageField(
        verbose_name=_('本地头像图片'),
        help_text=_('若留空, 则使用默认图片'),
        upload_to='uploads/avatars/%Y/%m/%d',
        null=True,
        blank=True
    )
    # avatar_thumbnail = ImageSpecField(
    #     source='avatar',
    #     processors=[ResizeToFill(64, 64)],
    #     format='JPEG',
    #     options={'quality': 80}
    # )

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.user.username


class Catagory(models.Model):
    parent = models.ForeignKey('self', default=None, blank=True, null=True, verbose_name='上级分类')

    name = models.CharField(max_length=30, verbose_name="分类名称")
    alias = models.CharField(max_length=40, verbose_name="英文名分类")

    status = models.IntegerField(default=0, choices=STATUS.items(), verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name="是否在导航位置显示")
    rank = models.IntegerField(default=0, verbose_name='展示排序')

    def __str__(self):
        if self.parent:
            return '%s:%s' %(self.parent, self.name)
        else:
            return '%s' %(self.name)

    class Meta:
        ordering = ['rank']
        verbose_name_plural = verbose_name = '分类'


class Blog(models.Model):
    author = models.ForeignKey(User, null=True,blank=True, verbose_name='作者')
    catagory = models.ForeignKey(Catagory, null=True,blank=True,related_name="blog_catagory", verbose_name="分类")

    title = models.CharField(null=True,blank=True,max_length=200, verbose_name='标题')
    alias = models.CharField(null=True,blank=True,max_length=200, db_index=True, blank=True, null=True,
                             verbose_name="英文标题", help_text="做伪静态url用")
    tags = models.CharField(null=True,blank=True,max_length=100,null=True,blank=True,
                                  verbose_name="标签",help_text="用英文逗号分割")
    status = models.IntegerField(null=True,blank=True,default=0,choices=STATUS.items(),verbose_name="状态")
    is_top = models.BooleanField(null=True,blank=True,default=False, verbose_name="置顶")

    summary = models.TextField(null=True,blank=True,verbose_name="摘要",max_length=1500)
    content = models.TextField(null=True,blank=True,verbose_name='文章正文rst/md格式', max_length=20000)
    content_html = models.TextField(null=True,blank=True,verbose_name="文章正文html",max_length=500)

    view_times = models.IntegerField(default=0,null=True,blank=True, verbose_name="浏览次数")
    pub_time = models.DateTimeField(default=datetime.datetime.now, null=True,blank=True,verbose_name="发布时间")
    create_time = models.DateTimeField(default=datetime.datetime.now, null=True,blank=True,editable=True, verbose_name='创建时间')
    update_time = models.DateTimeField(default=datetime.datetime.now, null=True,blank=True,verbose_name="更新时间")
    is_md = models.BooleanField(default=False,null=True,blank=True,verbose_name="是否为mardown格式")
    is_old = models.BooleanField(default=False,null=True,blank=True,verbose_name="是否为旧数据")

    blog_url = models.URLField(null=True,blank=True,verbose_name="链接地址")

    def __str__(self):
        return self.title

    def tags_list(self):
        return[tag.strip() for tag in sef.tag.split(',')]

    def get_absolute_url(self):
        return '%s/%s.html' %(setting.DOMAIN, self.alias)

    def next_post(self):
        return Post.objects.filter(id__gt=self.id, status=0).order_by('id').first()

    def prev_post(self):
        return Post.objects.filter(id__lt=self.id, status=0).first()

    def get_recently_posts(cls,num):
        return cls.object.values('title','alias').filter(status=0).order_by('-create_time')[:num]

    def related_posts(self):
        related_posts = None
        try:
            related_posts = Post.objects.values('title','alias').\
            filter(tags__icontains = self.tags_list()[0]).exclude(id=self.id)[:10]

        except IndexError:
            pass

        if not related_posts:
            related_posts = Post.objects.values('title','alias').\
                filter(catagory=self.catagory).\
                exclude(id=self.id)[:10]
        return related_posts

    class Meta:
        ordering = ['-is_top','-pub_time','-create_time']
        verbose_name_plural = verbose_name = "文章"


def check_or_update_post_alias(sender,instance = None, **kwargs):
    if not instance.alias:
        instance.alias = instance.id
        instance.save()


class Comment(models.Model):

    blog = models.ForeignKey(Blog,verbose_name='文章')
    name = models.ForeignKey(User,verbose_name='评论人')
    content = models.TextField(max_length=240, verbose_name='评论内容')
    created = models.DateTimeField(verbose_name='评论时间',default=datetime.datetime.now)

    def __str__(self):
        return self.content



