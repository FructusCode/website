from django.contrib import admin
from website.apwan.models.donation import Donation
from website.apwan.models.entity import Entity
from website.apwan.models.payee import Payee
from website.apwan.models.recipient import Recipient

__author__ = 'Dean Gardiner'


class DonationAdmin(admin.ModelAdmin):
    pass
admin.site.register(Donation, DonationAdmin)


class EntityAdmin(admin.ModelAdmin):
    pass
admin.site.register(Entity, EntityAdmin)


class PayeeAdmin(admin.ModelAdmin):
    pass
admin.site.register(Payee, PayeeAdmin)


class RecipientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Recipient, RecipientAdmin)