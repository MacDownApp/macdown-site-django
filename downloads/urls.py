from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^latest/$', views.latest, name='latest'),
    url(r'^v(?P<short_version>\d+(?:\.\w+)+)/$', views.version,
        name='short_version'),
    url(r'^(?P<version>[\.\d]+)/$', views.version, name='version'),
)
