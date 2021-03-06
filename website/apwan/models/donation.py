from django.db import models
from website.apwan.core.database import sql_auto_increment
from website.apwan.models.entity import Entity
from website.apwan.models.token import Token

__author__ = 'Dean Gardiner'


class Donation(models.Model):
    class Meta:
        app_label = 'apwan'

    STATE_NEW = 'new'
    STATE_AUTHORIZED = 'authorized'
    STATE_RESERVED = 'reserved'
    STATE_CAPTURED = 'captured'
    STATE_SETTLED = 'settled'
    STATE_CANCELLED = 'cancelled'
    STATE_REFUNDED = 'refunded'
    STATE_CHARGEBACK = 'charged back'
    STATE_FAILED = 'failed'
    STATE_EXPIRED = 'expired'

    STATES = (
        (STATE_NEW, "New"),
        (STATE_AUTHORIZED, "Authorized"),
        (STATE_RESERVED, "Reserved"),
        (STATE_CAPTURED, "Captured"),
        (STATE_SETTLED, "Settled"),
        (STATE_CANCELLED, "Cancelled"),
        (STATE_REFUNDED, "Refunded"),
        (STATE_CHARGEBACK, "Charged Back"),
        (STATE_FAILED, "Failed"),
        (STATE_EXPIRED, "Expired"),
    )

    CURRENCY_USD = 0

    CURRENCIES = (
        (CURRENCY_USD, "USD"),
    )

    entity = models.ForeignKey(Entity)
    recipient = models.ForeignKey('Recipient', null=True)
    payee = models.ForeignKey('Payee', null=True)

    token = models.CharField(unique=True, blank=True, max_length=32)

    state = models.CharField(max_length=12, choices=STATES, default=STATE_NEW)

    # TODO: "payer_name" can be replaced with user accounts
    payer_name = models.CharField(max_length=64, default="Anonymous")

    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tip = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    currency = models.IntegerField(choices=CURRENCIES, default=CURRENCY_USD)

    # Following fields use dependant on payee payment platform
    # TODO: Rename 'checkout_id' to 'transaction_id'
    checkout_id = models.CharField(max_length=18, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.token == '':
            next_id = sql_auto_increment(Donation)
            self.token = Token.create_token(next_id)

        super(Donation, self).save(*args, **kwargs)
