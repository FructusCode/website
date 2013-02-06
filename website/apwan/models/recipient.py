from django.contrib.auth.models import User
from django.db import models
from website.apwan.core.database import unique_slugify
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

    owner = models.ForeignKey(User, null=True, blank=True)
    payee = models.ForeignKey(Payee, null=True, blank=True)

    title = models.CharField(max_length=64)  # TODO: Is 64 large enough?
    s_title = models.CharField(max_length=64)  # Search Field
    slug = models.SlugField(max_length=64, blank=True)

    type = models.IntegerField(choices=TYPES)

    def path(self):
        return '/account/recipient/' + self.slug

    def save(self, **kwargs):
        unique_slugify(
            self, self.title
        )
        super(Recipient, self).save(kwargs)

    def dict(self,
             entities_include=False, entities_filter=None, entities_limit=None,
             check_owner=None,
             payee_include=False):
        """Return a safe dict of the modal data

        entities_include -- include recipient entities in result (adds 'entities' key [list])
        entities_filter  -- entity query filter
        entities_limit   -- max number of entities to return (adds 'entities_more' [int] when applicable)

        check_owner      -- checks if the check_owner [User] instance is the owner of this recipient
                            (adds 'owned' key [bool])

        payee_include    -- include payee in result
        """
        item = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'type': self.type,
            'type_label': self.get_type_display(),
            'claimed': self.owner is not None
        }

        # Include Entities
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

        # Check Owner
        if check_owner is not None:
            item['owned'] = self.owner == check_owner

        # Include Payee
        if payee_include:
            if self.payee:
                item['payee'] = self.payee.dict()
            else:
                item['payee'] = None

        return item

    def __unicode__(self):
        return self.title