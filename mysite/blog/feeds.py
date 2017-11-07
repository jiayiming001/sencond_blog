#-*- coding:utf-8 -*-
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
from django.utils.safestring import mark_safe
import markdown

class LatestPostFeed(Feed):
    title = 'My blog'
    link = '/blog/'
    description_template = 'New posts of my blog'

    def items(self):
        return Post.published.all()[:3]

    def item_title(self, item):
        return mark_safe(markdown.markdown(item.title))

    def item_description(self, item):
        return mark_safe(markdown.markdown(truncatewords(item.body, 30)))