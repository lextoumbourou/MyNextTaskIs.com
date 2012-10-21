from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from django.utils.translation import ugettext_lazy as _


class UserCreationForm(UserCreationFormBase):
    """
    Class passed into lazysignup view to override default and allow
    for email address username
    """
    username = forms.EmailField(label=_("Email"),
        help_text = _("Required. A valid email address."),
        error_messages = {
            'invalid': _("That doesn't appear to be a valid email address.")})

    def get_credentials(self):
        return {
            "username": self.cleaned_data["username"],
            "password": self.cleaned_data["password1"]}

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        # Set the email to the same thing as the username 
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user
