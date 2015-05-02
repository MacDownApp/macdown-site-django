from django.conf.urls import patterns, url
from .views import channel

urlpatterns = patterns(
    '',
    url(r'^(?P<app_slug>[\w-]+)/appcast\.xml$', channel,
        name='sparkle_application_default_channel'),
    url(r'^(?P<app_slug>[\w-]+)/(?P<channel_slug>[\w-]+)/appcast\.xml$',
        channel, name='sparkle_application_channel')
)
