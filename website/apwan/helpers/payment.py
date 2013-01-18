from django.db import IntegrityError
from wepay import WePay
from website.apwan.models.payee import Payee
from website.keys import WEPAY_PRODUCTION, WEPAY_ACCESS_TOKEN, WEPAY_CLIENT_ID, WEPAY_CLIENT_SECRET

__author__ = 'Dean Gardiner'


class PaymentPlatform():
    def create_payee(self, owner, type, token):
        try:
            Payee.objects.create(owner=owner, type=type, token=token, name="My Payee")
        except IntegrityError, e:
            return False
        return True


class WePayPaymentPlatform(PaymentPlatform):
    def __init__(self):
        self.wepay = WePay(
            production=WEPAY_PRODUCTION,
            store_token=False
        )

    def get_authorization_url(self, callback_url, scope="manage_accounts,collect_payments,view_user"):
        return self.wepay.get_authorization_url(
            callback_url, WEPAY_CLIENT_ID, scope=scope
        )

    def store_token(self, owner, callback_url, code):
        token_response = self.wepay.get_token(
            callback_url, WEPAY_CLIENT_ID,
            WEPAY_CLIENT_SECRET, code
        )
        return self.create_payee(owner, Payee.TYPE_WEPAY, token_response['access_token'])

wepay = WePayPaymentPlatform()