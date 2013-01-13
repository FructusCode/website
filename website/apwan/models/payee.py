from django.contrib.auth.models import User
from django.db import models

__author__ = 'Dean Gardiner'


class Payee(models.Model):
    class Meta:
        app_label = 'apwan'

    TYPE_WEPAY = 0

    TYPES = (
        (TYPE_WEPAY, "WePay"),
    )

    owner = models.ForeignKey(User)
    type = models.IntegerField(choices=TYPES)
    account_id = models.IntegerField()  # WePay account_id