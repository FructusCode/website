# pylint: disable=R0904

from django.contrib import admin
from website.apwan.models.donation import Donation

__author__ = 'Dean Gardiner'


class DonationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'recipient', 'state', 'payer_name',
        'amount', 'tip', 'currency'
    )
admin.site.register(Donation, DonationAdmin)
