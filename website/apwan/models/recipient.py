from django.contrib.auth.models import User
from django.db import models
from website.apwan.models.payee import Payee

__author__ = 'Dean Gardiner'


class Recipient(models.Model):
    class Meta:
        app_label = 'apwan'

    # Music
    TYPE_M_LABEL = 0
    TYPE_M_ARTIST = 1

    TYPES = (
        (TYPE_M_LABEL, "Label"),
        (TYPE_M_ARTIST, "Artist"),
    )

    owner = models.ForeignKey(User, null=True)
    payee = models.ForeignKey(Payee, null=True)
    title = models.CharField(max_length=64)
    type = models.IntegerField(choices=TYPES)

    def dict(self):
        return {
            'title': self.title,
            'type': self.type
        }