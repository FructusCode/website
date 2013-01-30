from django.contrib.auth.models import User
from django.db import models
from website.apwan.models.entity import Entity
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
    s_title = models.CharField(max_length=64)  # Search Field
    type = models.IntegerField(choices=TYPES)

    def dict(self, entities_include=False, entities_filter=None, entities_limit=None):
        item = {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'type_label': self.get_type_display()
        }

        if entities_include:
            if entities_filter is None:
                entities_filter = {}
            item['entities'] = []
            if entities_limit is not None:
                entities = Entity.objects.all().filter(recipient=self, **entities_filter)[:entities_limit]
                entity_count = Entity.objects.all().filter(recipient=self, **entities_filter).count()
                if entity_count > entities_limit:
                    item['entities_more'] = entity_count - entities_limit
            else:
                entities = Entity.objects.all().filter(recipient=self, **entities_filter)
            for entity in entities:
                item['entities'].append(entity.dict())

        return item

    def __unicode__(self):
        return self.title