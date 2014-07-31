from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.post_list, name='list'),
    url(r'^(?P<id>\d+)/$', views.post_detail),
    url(r'^(?P<id>\d+)/(?P<slug>.+?)/$', views.post_detail, name='post'),
)
