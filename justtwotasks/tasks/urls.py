from django.conf.urls import patterns, include, url

urlpatterns = patterns('justtwotasks.tasks.views',
    url(r'^task/(?P<task>\d+)/?$', 'request_dispatcher'),
    url(r'^task/?$', 'request_dispatcher'),
    url(r'^get_tasks', 'get_tasks'),
    url(r'^update_task', 'update_task'),
    url(r'^', 'main'),
)
