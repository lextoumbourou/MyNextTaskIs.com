from django.conf.urls import patterns, include, url

urlpatterns = patterns('justtwotasks.tasks.views',
    url(r'^', 'main'),
)
