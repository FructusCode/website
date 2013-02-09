from django.db import models
from website.apwan.core import string_length_limit

__author__ = 'Dean Gardiner'


class Entity(models.Model):
    class Meta:
        app_label = 'apwan'
        verbose_name_plural = 'entities'

    TYPE_TVSHOW = 0
    TYPE_MOVIE = 1
    TYPE_MUSIC = 2
    TYPE_GAME = 3

    TYPES = (
        (TYPE_TVSHOW, "TV Show"),
        (TYPE_MOVIE, "Movie"),
        (TYPE_MUSIC, "Music"),
        (TYPE_GAME, "Game"),
    )

    recipient = models.ManyToManyField('Recipient')

    parent = models.ForeignKey('self', null=True)

    # for TYPE_TVSHOW, TYPE_MOVIE, TYPE_GAME
    title = models.CharField(max_length=64, null=True)

    # for TYPE_MOVIE
    year = models.IntegerField(max_length=4, null=True)

    # for TYPE_MUSIC
    artist = models.CharField(max_length=64, null=True)
    album = models.CharField(max_length=64, null=True)
    track = models.CharField(max_length=64, null=True)

    # Search fields
    s_title = models.CharField(max_length=64, null=True)
    s_artist = models.CharField(max_length=64, null=True)
    s_album = models.CharField(max_length=64, null=True)
    s_track = models.CharField(max_length=64, null=True)

    image = models.CharField(max_length=64, null=True)
    type = models.IntegerField(choices=TYPES)
    suggested_amount = models.DecimalField(max_digits=8, decimal_places=2,
                                           null=True)

    def description(self, max_length=-1):
        desc = ""
        if self.type == Entity.TYPE_MUSIC:
            if self.track:
                desc = self._join_limit(" - ", [
                    self.track, self.album, self.artist
                ], max_length)
            elif self.album:
                desc = self._join_limit(" - ", [
                    self.album, self.artist
                ], max_length)
            else:
                desc = string_length_limit(self.artist, max_length)
        else:
            desc = string_length_limit(self.title, max_length)

        return desc

    @staticmethod
    def _join_limit(sep, iterable, max_length):
        text = sep.join(iterable)
        total_sep_length = len(iterable) * len(sep)
        if max_length == -1 or len(text) < max_length - total_sep_length:
            return text

        each_limit = (max_length - total_sep_length) / len(iterable)
        trimmed_items = []
        for item in iterable:
            trimmed_items.append(string_length_limit(item, each_limit))
        return sep.join(trimmed_items)

    def dict(self, full=False):
        item = {
            'id': self.id,
            'image': self.image,
            'type': self.type
        }
        if self.type == self.TYPE_MUSIC:
            item['artist'] = self.artist

            if self.album is not None:
                item['album'] = self.album

            if self.track is not None:
                item['track'] = self.track
        else:
            item['title'] = self.title

            if self.type == self.TYPE_MOVIE:
                item['year'] = self.year

        if full:
            item['recipients'] = []
            # pylint: disable=E1101
            for recipient in self.recipient.all():
                item['recipients'].append(recipient.dict())
            # pylint: enable=E1101

        return item

    def __unicode__(self):
        prefix = "[%s] " % Entity.TYPES[self.type][1]
        if self.type == Entity.TYPE_MUSIC:
            if self.track:
                prefix += "[Track] "
            elif self.album:
                prefix += "[Album] "
            else:
                prefix += "[Artist] "

        return prefix + self.description()
