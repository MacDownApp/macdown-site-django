from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.all_, name='all'),
    url(r'^(?P<slug>[\w-]+)/$', views.channel, name='channel'),
)
