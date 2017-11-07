from django.conf.urls import url
import views

from .feeds import LatestPostFeed

urlpatterns = [
    url(r'^$', views.post_list, name= 'post_list'),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<post>[-\w\s*]+)/$',
       view=views.post_detail, name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', views.post_share, name='post_share'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$',views.post_list,name='post_list_by_tag'),
    url(r'^feed/$',LatestPostFeed(), name='post_feed'),
]
