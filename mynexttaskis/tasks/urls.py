from django.conf.urls import patterns, include, url

urlpatterns = patterns('mynexttaskis.tasks.views',
    url(r'^api/task/?(?P<task>\d+)?/?$', 'request_dispatcher'),
    url(r'^', 'main'),
)
