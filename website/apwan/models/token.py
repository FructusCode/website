import hashlib
import datetime
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
        if self.token == '':
            next_id = sql_auto_increment(Token)
            md5 = hashlib.md5()

            # pylint: disable=E1101
            md5.update(settings.SECRET_SALT)
            md5.update(str(next_id))
            # pylint: enable=E1101

            self.token = md5.hexdigest()

        super(Token, self).save(*args, **kwargs)

    def __str__(self):
        return "[Token %s]" % self.token
