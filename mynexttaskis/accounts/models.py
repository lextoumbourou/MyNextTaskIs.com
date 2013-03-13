import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from timezones.zones import COMMON_TIMEZONE_CHOICES

from mynexttaskis.accounts import signals


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    timezone = models.CharField(
        max_length=255, choices=COMMON_TIMEZONE_CHOICES, blank=True, null=True)
    day_ends = models.TimeField(default=datetime.time(06, 00))


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
