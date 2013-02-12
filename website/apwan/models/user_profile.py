from django.contrib.auth.models import User
from django.db import models
from website.apwan.core.deployauth import deployauth_token_update

__author__ = 'Dean Gardiner'


class UserProfile(models.Model):
    class Meta:
        app_label = 'apwan'

    CONTACT_METHOD_EMAIL = 0
    CONTACT_METHOD_PHONE = 1
    CONTACT_METHODS = (
        (CONTACT_METHOD_EMAIL, "Email"),
        (CONTACT_METHOD_PHONE, "Phone"),
    )

    user = models.ForeignKey(User)

    preferred_contact_method = models.IntegerField(
        choices=CONTACT_METHODS, default=CONTACT_METHOD_EMAIL)

    deployauth_token = models.CharField(max_length=128, blank=True,
                                        verbose_name="DeployAuth Token")

    def save(self, **kwargs):
        deployauth_token_update(self)
        super(UserProfile, self).save(kwargs)
