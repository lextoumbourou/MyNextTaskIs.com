from django.dispatch import receiver
from django.core.mail import mail_admins

from lazysignup.signals import converted

@receiver(converted)
def notify_admins_of_registration(sender, **kwargs):
    subject = "{0} just signed up for My Next Task Is".format(
        kwargs['user'].username)
    mail_admins(subject, "")
