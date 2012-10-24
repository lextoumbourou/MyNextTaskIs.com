from django.conf.urls import patterns, include, url

urlpatterns = patterns('justtwotasks.tasks.views',
    url(r'^delete_task', 'delete_task'),
    url(r'^complete_task', 'complete_task'),
    url(r'^add_tasks', 'add_tasks'),
    url(r'^', 'main'),
)
