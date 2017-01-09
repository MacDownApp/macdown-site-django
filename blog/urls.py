from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from . import feeds, views

urlpatterns = patterns(
    '',
    url(r'^$', views.post_list, name='list'),
    url(r'^post/(?P<id>\d+)/$', views.post_detail),
    url(r'^post/(?P<id>\d+)/(?P<slug>.+?)/$', views.post_detail, name='post'),

    url(r'^feed/atom\.xml$', feeds.atom1, name='atom1'),

    # Deprecated.
    url(r'^feed/rss201rev2/$', feeds.rss201rev2, name='rss201rev2'),
    url(r'^feed/atom1/$', RedirectView.as_view(
        url=reverse_lazy('blog:atom1'), permanent=True,
    )),
)
