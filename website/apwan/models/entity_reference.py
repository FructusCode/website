from django.db import models
from website.apwan.models.entity import Entity

__author__ = 'Dean Gardiner'


class EntityReference(models.Model):
    class Meta:
        app_label = 'apwan'

    TYPE_MUSICBRAINZ = 0

    TYPES = (
        (TYPE_MUSICBRAINZ, "MusicBrainz"),
    )

    entity = models.ForeignKey(Entity)

    type = models.IntegerField(choices=TYPES)
    key = models.CharField(max_length=64, unique=True)