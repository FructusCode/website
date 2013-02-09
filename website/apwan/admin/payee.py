# pylint: disable=R0904

from django.contrib import admin
from django.core.urlresolvers import reverse
from website.apwan.models.payee import Payee

__author__ = 'Dean Gardiner'


class PayeeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'title', 'slug', 'user_link')
    list_display_links = ('title',)

    def user_link(self, obj):
        if obj.user is None:
            return obj.user
        url = reverse('admin:apwan_service_changelist')
        return '<a href="%s?id=%s">%s</a>' % (url, obj.user_id, obj.user)
    user_link.short_description = "User"
    user_link.allow_tags = True
admin.site.register(Payee, PayeeAdmin)
