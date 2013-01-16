from django.contrib.auth.models import User
from django.db import models
from website.apwan.models.payee import Payee

__author__ = 'Dean Gardiner'


class Recipient(models.Model):
    class Meta:
        app_label = 'apwan'

    # Music
    TYPE_MUSIC_LABEL = 0
    TYPE_MUSIC_ARTIST = 1
    # Movie
    TYPE_MOVIE_PRODUCTION_COMPANY = 2

    TYPES = (
        (TYPE_MUSIC_LABEL, "Label"),
        (TYPE_MUSIC_ARTIST, "Artist"),
        (TYPE_MOVIE_PRODUCTION_COMPANY, "Production Company"),
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

    def __unicode__(self):
        return self.title