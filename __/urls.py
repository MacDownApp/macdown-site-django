from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^sparkle/', include('sparkle.urls')),
    url(r'^download/', include('downloads.urls', namespace='downloads')),
    url(r'^blog/', include('blog.urls', namespace='blog')),
    url(r'^history/', include('history.urls', namespace='history')),
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('pages.urls', namespace='pages')),
)
