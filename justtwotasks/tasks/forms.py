from django import forms
from emailusernames.forms import EmailUserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserCreationForm(EmailUserCreationForm):
    """
    Class passed into lazysignup view to override default and allow
    for email address username
    """
    def get_credentials(self):
        return {
            "email": self.cleaned_data["email"],
            "password": self.cleaned_data["password1"]}

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        # Set the email to the same thing as the username 
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
