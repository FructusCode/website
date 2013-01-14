from django.db import models
from website.apwan.models.recipient import Recipient

__author__ = 'Dean Gardiner'


class RecipientReference(models.Model):
    class Meta:
        app_label = 'apwan'

    TYPE_MUSICBRAINZ = 0

    TYPES = (
        (TYPE_MUSICBRAINZ, "MusicBrainz"),
    )

    recipient = models.ForeignKey(Recipient)

    type = models.IntegerField(choices=TYPES)
    key = models.CharField(max_length=64, unique=True)