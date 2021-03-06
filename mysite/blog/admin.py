# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Post,Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slug','author','publish','status',)
    list_filter = ('status','created','publish','author',)
    search_fields = ('title','body',)
    prepopulated_fields = {'slug':('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status','publish']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('post','name','email','body','active')
    list_filter = ('active','created')
    search_fields = ('post','body','email','name')
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post,PostAdmin)