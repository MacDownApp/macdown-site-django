from django.conf.urls import patterns, url
from . import feeds, views

urlpatterns = patterns(
    '',
    url(r'^$', views.post_list, name='list'),
    url(r'^post/(?P<id>\d+)/$', views.post_detail),
    url(r'^post/(?P<id>\d+)/(?P<slug>.+?)/$', views.post_detail, name='post'),
    url(r'^feed/rss201rev2/$', feeds.rss201rev2, name='rss201rev2'),
    url(r'^feed/atom1/$', feeds.atom1, name='atom1'),
)
