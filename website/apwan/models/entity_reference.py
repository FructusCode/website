from django.db import models
from website.apwan.models.entity import Entity

__author__ = 'Dean Gardiner'


class EntityReference(models.Model):
    class Meta:
        app_label = 'apwan'

    TYPE_MUSICBRAINZ = 0
    TYPE_THEMOVIEDB = 1

    TYPES = (
        (TYPE_MUSICBRAINZ, "MusicBrainz"),
        (TYPE_THEMOVIEDB, "The Movie Database"),
    )

    entity = models.ForeignKey(Entity)

    type = models.IntegerField(choices=TYPES)
    key = models.CharField(max_length=64, unique=True)
