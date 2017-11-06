# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from taggit.managers import TaggableManager
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='publish')
# Create your models here.
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('publish','Publish'),
    )
    title = models.CharField(max_length=250, verbose_name='标题')
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish',verbose_name = '标记')
    author = models.ForeignKey(User,related_name='blog_posts',verbose_name= '作者')
    body = models.TextField(verbose_name='内容')
    publish = models.DateTimeField(default=timezone.now(),verbose_name='发布时间')
    created = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True,verbose_name='更新时间')
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft',verbose_name='状态')
    tags = TaggableManager()
    objects = models.Manager()
    published = PublishedManager()
    class Meta:
        ordering = ['-publish']
        verbose_name = '文章'
        verbose_name_plural = '文章'
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])  # .../blog/2017/11/4/(slug)

class Comment(models.Model):
    post = models.ForeignKey(Post,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        verbose_name_plural='评论'
        verbose_name='评论'

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)



