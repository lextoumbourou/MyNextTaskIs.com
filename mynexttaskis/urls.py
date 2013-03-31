from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from accounts.forms import ProfileForm, UserCreationForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profiles/create/?', 'profiles.views.create_profile', {'success_url': '/'}),
    url(r'^profiles/edit/?', 'profiles.views.edit_profile', {'form_class': ProfileForm,
                                                             'success_url': '/'}),
    url(r'^convert', include('lazysignup.urls'), {'form_class' : UserCreationForm}),
    url(r'^robots.txt', direct_to_template,
        {'template': 'robots.txt', 'mimetype': 'text/plain'}),
    url(r'^humans.txt', direct_to_template,
        {'template': 'humans.txt', 'mimetype': 'text/plain'}),
    url(r'^api/', include('mynexttaskis.tasks.urls')),
    
    url(r'^about/?', direct_to_template, {
        'template': 'about.html'
    }),
    url(r'^/?', direct_to_template, {
        'template': 'parent.html'
    }),
)
