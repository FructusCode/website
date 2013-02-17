import datetime
from django.contrib import admin
import pytz
from website.apwan.models.token import Token

__author__ = 'Dean Gardiner'


class TokenAdmin(admin.ModelAdmin):
    list_display = (
        'owner',
        'token', 'token_type',
        'expires_in'
    )
    list_display_links = ('token',)

    def expires_in(self, obj):
        expire_delta = obj.expire - datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        expire_seconds = expire_delta.total_seconds()
        expire_minutes = round(expire_seconds / 60, 0)
        expire_hours = round(expire_minutes / 60, 0)

        if expire_hours > 1:
            return "%d hours" % expire_hours
        elif expire_hours == 1:
            return "1 hour"
        elif expire_minutes > 1:
            return "%d minutes" % expire_minutes
        elif (expire_seconds / 60) == 1:
            return "1 minute"
        elif expire_seconds > 1:
            return "%d seconds" % expire_seconds
        elif expire_seconds == 1:
            return "1 second"
        else:
            return "EXPIRED"

admin.site.register(Token, TokenAdmin)
