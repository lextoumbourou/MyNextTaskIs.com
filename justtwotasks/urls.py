from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tasks.forms import UserCreationForm
from emailusernames.forms import EmailAuthenticationForm

from justtwotasks.accounts.forms import ProfileForm

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin', include(admin.site.urls)),
    url(r'^accounts/login/?', auth_views.login,
        {'template_name': 'registration/login.html',
         'authentication_form':EmailAuthenticationForm}, name='login'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profiles/create/?', 'profiles.views.create_profile', {'success_url': '/'}),
    url(r'^profiles/edit/?', 'profiles.views.edit_profile', {'form_class': ProfileForm,
                                                             'success_url': '/'}),
    url(r'^convert', include('lazysignup.urls'), {'form_class' : UserCreationForm}),
    url(r'^', include('justtwotasks.tasks.urls')),
)
