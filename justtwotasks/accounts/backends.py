from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import validate_email as vd
from django.core.exceptions import ValidationError


class EmailOrUsernameModelBackend(object):
    """
    Authenticate a user using either a username or email address
    """
    def authenticate(self, username=None, password=None):
        if validate_email(username):
            kwargs = {'email':username}
        else:
            kwargs = {'username':username}

        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

def validate_email(email):
    """
    Return BOOL depending on validity of email
    """
    try:
        vd(email)
        return True
    except ValidationError:
        return False

