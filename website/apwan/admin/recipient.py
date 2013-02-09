from django.contrib import admin
from django.core.urlresolvers import reverse
from website.apwan.models.recipient import Recipient
from website.apwan.models.recipient_reference import RecipientReference

__author__ = 'Dean Gardiner'


class RecipientAdmin(admin.ModelAdmin):
    list_display = ('type', 'title', 'slug')
    list_display_links = ('title',)
admin.site.register(Recipient, RecipientAdmin)


class RecipientReferenceAdmin(admin.ModelAdmin):
    list_display = ('recipient_link', 'type', 'key')
    list_display_links = ('key',)

    def recipient_link(self, obj):
        url = reverse('admin:apwan_recipient_changelist')
        return '<a href="%s?id=%s">%s</a>' % (
            url, obj.recipient_id, obj.recipient
        )
    recipient_link.allow_tags = True
admin.site.register(RecipientReference, RecipientReferenceAdmin)
