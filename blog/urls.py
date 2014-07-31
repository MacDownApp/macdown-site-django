from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^(?P<id>\d+)/$', views.post),
    url(r'^(?P<id>\d+)/(?P<slug>.+?)/$', views.post, name='post'),
)
