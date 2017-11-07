# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Post,Comment
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
# Create your views here.
"""
def post_list(request):
    object_list = Post.objects.all()
    paginator = Paginator(object_list,2) #3篇文章为一页
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = Paginator.page(paginator.num_pages)
    return render(request,
                  'list.html',
                  {'posts':posts,
                   'page':page})

class PostListView(ListView):
    queryset = Post.objects.all()
    context_object_name = 'posts'
    paginate_by = 2
    template_name = 'list.html'
    tag = None
"""

def post_list(request, tag_slug=None):
    object_list = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list,2)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
        page = 1
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        page = paginator.num_pages
    return render(request,'list.html',{'page':page,
                                       'posts':posts,
                                       'tag':tag })



def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                    status='publish',
                                    publish__year=year,
                                    publish__month=month,
                                    publish__day=day)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.all().filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'mysite/detail.html', {'post':post,
                                                  'comments':comments,
                                                  'new_comment':new_comment,
                                                  'comment_form':comment_form,
                                                  'similar_posts':similar_posts})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{}({}) recommends you reading "{}" '.format(cd['name'],cd['email'],post.title)
            message = 'Read "{}" at {} \n\n{}\'s comments: {}'.format(post.title,post_url,cd['name'],cd['comments'])
            send_mail(subject,message,'15858830567m@sina.cn',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'share.html',{'post':post,
                                         'form':form,
                                         'sent':sent})