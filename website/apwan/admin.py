from django.contrib import admin
from django.core.urlresolvers import reverse
from website.apwan.models.donation import Donation
from website.apwan.models.entity import Entity
from website.apwan.models.entity_reference import EntityReference
from website.apwan.models.payee import Payee
from website.apwan.models.recipient import Recipient
from website.apwan.models.recipient_reference import RecipientReference

__author__ = 'Dean Gardiner'


class DonationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Donation, DonationAdmin)


class EntityAdmin(admin.ModelAdmin):
    list_display = ('entity_title', 'image', 'suggested_amount')

    def entity_title(self, obj):
        return obj.__unicode__()
    entity_title.short_description = 'Title'

admin.site.register(Entity, EntityAdmin)


class EntityReferenceAdmin(admin.ModelAdmin):
    list_display = ('entity_link', 'type', 'key',)
    list_display_links = ('key',)

    def entity_link(self, obj):
        url = reverse('admin:apwan_entity_changelist')
        return '<a href="%s?id=%s">%s</a>' % (url, obj.entity_id, obj.entity)
    entity_link.allow_tags = True
admin.site.register(EntityReference, EntityReferenceAdmin)


class PayeeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Payee, PayeeAdmin)


class RecipientAdmin(admin.ModelAdmin):
    list_display = ('type', 'title')
    list_display_links = ('title',)
admin.site.register(Recipient, RecipientAdmin)


class RecipientReferenceAdmin(admin.ModelAdmin):
    list_display = ('recipient_link', 'type', 'key',)
    list_display_links = ('key',)

    def recipient_link(self, obj):
        url = reverse('admin:apwan_recipient_changelist')
        return '<a href="%s?id=%s">%s</a>' % (url, obj.recipient_id, obj.recipient)
    recipient_link.allow_tags = True
admin.site.register(RecipientReference, RecipientReferenceAdmin)