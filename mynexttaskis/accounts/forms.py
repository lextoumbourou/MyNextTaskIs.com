from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from mynexttaskis.accounts.models import UserProfile


class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        try:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
        except User.DoesNotExist:
            pass

    first_name = forms.CharField(max_length=60, help_text='Enter your first name')
    last_name = forms.CharField(max_length=60, help_text='Enter your last name')

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'timezone', 'day_ends',)

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(ModelForm, self).save(*args, **kwargs)
        return profile

class UserCreationForm(BaseUserCreationForm):
    """
    Class passed into lazysignup view to override default and allow
    for email address username
    """
    email = forms.EmailField(label=_('Email'),
                             help_text = _('Required. A valid email address.'),
                             error_messages = {
                                 'invalid': _("That doesn't appear to be a valid email address.")})

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email',)

    def get_credentials(self):
        return {
            "username": self.cleaned_data["username"],
            "password": self.cleaned_data["password1"]}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'A user has already registered with this email address.')
        return email
