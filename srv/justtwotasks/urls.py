from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin', include(admin.site.urls)),
    url(r'^accounts/', include('registration.urls')),
    url(r'^convert', include('lazysignup.urls')),
    url(r'^', include('justtwotasks.tasks.urls')),
)
