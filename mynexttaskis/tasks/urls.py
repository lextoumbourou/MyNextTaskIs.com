from django.conf.urls import patterns, include, url

urlpatterns = patterns('mynexttaskis.tasks.views',
    url(r'^task/?(?P<task>\S+)?/?$', 'request_dispatcher'),
)
