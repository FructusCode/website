import hashlib
import datetime
import time
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from json_field import JSONField
import pytz
from website.apwan.core.database import sql_auto_increment

__author__ = 'Dean Gardiner'


class Token(models.Model):
    class Meta:
        app_label = 'apwan'

    TOKEN_RECIPIENT_LOOKUP = 1
    TOKENS = (
        (TOKEN_RECIPIENT_LOOKUP, "Recipient Lookup"),
    )

    owner = models.ForeignKey(User, null=True, blank=True)

    token = models.CharField(unique=True, blank=True, max_length=32)
    token_type = models.IntegerField(choices=TOKENS, default=0)

    data = JSONField(null=True, blank=True)

    expire = models.DateTimeField(null=True, blank=True)

    def valid(self, expire_delete=True):
        if self.expire > datetime.datetime.utcnow().replace(tzinfo=pytz.utc):
            return True

        if expire_delete:
            self.delete()
        return False

    @staticmethod
    def create_token(value):
        if value is None or value == '':
            raise ValueError()

        md5 = hashlib.md5()

        # pylint: disable=E1101
        md5.update(settings.SECRET_SALT)
        md5.update(str(time.time()))
        md5.update(str(value))
        # pylint: enable=E1101

        return md5.hexdigest()

    def save(self, *args, **kwargs):
        if self.token == '':
            next_id = sql_auto_increment(Token)
            self.token = self.create_token(next_id)

        super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return "[Token %s]" % self.token
