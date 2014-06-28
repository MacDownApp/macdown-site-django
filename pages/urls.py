from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^features/$', views.features, name='features'),
    url(r'^faq/$', views.faq, name='faq'),
)
