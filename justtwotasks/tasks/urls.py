from django.conf.urls import patterns, include, url

urlpatterns = patterns('justtwotasks.tasks.views',
    url(r'^get_tasks', 'get_tasks'),
    url(r'^update_tasks', 'update_tasks'),
    url(r'^', 'main'),
)
