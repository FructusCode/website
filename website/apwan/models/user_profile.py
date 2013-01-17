from django.contrib.auth.models import User
from django.db import models

__author__ = 'Dean Gardiner'

class UserProfile(models.Model):
    class Meta:
        app_label = 'apwan'

    user = models.ForeignKey(User)