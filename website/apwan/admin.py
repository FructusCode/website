from django.contrib import admin
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
    pass
admin.site.register(Entity, EntityAdmin)


class EntityReferenceAdmin(admin.ModelAdmin):
    pass
admin.site.register(EntityReference, EntityReferenceAdmin)


class PayeeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Payee, PayeeAdmin)


class RecipientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Recipient, RecipientAdmin)


class RecipientReferenceAdmin(admin.ModelAdmin):
    pass
admin.site.register(RecipientReference, RecipientReferenceAdmin)