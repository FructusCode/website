import uuid
import datetime
from django.contrib.auth.models import User
from django.db import models
from json_field import JSONField
import pytz

__author__ = 'Dean Gardiner'


class Token(models.Model):
    class Meta:
        app_label = 'apwan'

    TOKEN_RECIPIENT_LOOKUP = 1
    TOKENS = (
        (TOKEN_RECIPIENT_LOOKUP, "Recipient Lookup"),
    )

    owner = models.ForeignKey(User, null=True, blank=True)

    token = models.CharField(unique=True, max_length=32)
    token_type = models.IntegerField(choices=TOKENS, default=0)

    data = JSONField(null=True, blank=True)

    expire = models.DateTimeField(null=True, blank=True)

    def valid(self, expire_delete=True):
        if self.expire > datetime.datetime.utcnow().replace(tzinfo=pytz.utc):
            return True

        if expire_delete:
            self.delete()
        return False

    def save(self, *args, **kwargs):
        # Create a token if one hasn't already been set
        if self.token == '':
            self.token = uuid.uuid4().hex

        super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return "[Token %s]" % self.token
