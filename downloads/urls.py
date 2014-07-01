from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^latest/$', views.latest, name='latest'),
    url(r'^v(?P<version>\d+(?:\.\w+)+)/$', views.version, name='version'),
)
