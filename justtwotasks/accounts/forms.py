from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User

from justtwotasks.accounts.models import UserProfile


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
