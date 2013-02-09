# pylint: disable=E0611
# pylint: disable=F0401
from django.db import IntegrityError
from wepay import WePay
from website.apwan.core import string_length_limit
from website.apwan.models.donation import Donation
from website.apwan.models.payee import Payee
from website.apwan.models.service import Service
from website.keys import (
    WEPAY_PRODUCTION,
    WEPAY_CLIENT_ID,
    WEPAY_CLIENT_SECRET
)
# pylint: enable=E0611
# pylint: enable=F0401

__author__ = 'Dean Gardiner'


class PaymentPlatform(object):
    DESC_FRUCTUS_TIP = " + Fruct.us Tip"

    def __init__(self):
        pass

    @staticmethod
    def db_payee_create(account, name="My Payee"):
        try:
            Payee.objects.create(
                owner=account.owner,
                account=account,
                name=name
            )
        except IntegrityError:
            return False
        return True

    @staticmethod
    def db_donation_create(entity, recipient, payee,
                           amount, currency=Donation.CURRENCY_USD, tip=0.0,
                           payer_name="Anonymous"):
        try:
            return Donation.objects.create(
                entity=entity,
                recipient=recipient,
                payee=payee,

                amount=amount,
                currency=currency,
                tip=tip,

                payer_name=payer_name,
                state=Donation.STATE_NEW
            )
        except IntegrityError:
            return None

    @staticmethod
    def db_service_create(owner, service, service_id, link_type, data):
        try:
            return Service.objects.create(
                owner=owner,

                service=service,
                service_id=service_id,
                service_type=Service.TYPE_PAYEE_USER,

                link_type=link_type,
                data=data
            )
        except IntegrityError:
            return None


class WePayPaymentPlatform(PaymentPlatform):
    DEFAULT_AUTH_SCOPE = "manage_accounts,collect_payments,view_user"

    def __init__(self):
        super(WePayPaymentPlatform, self).__init__()
        self.wepay = WePay(
            production=WEPAY_PRODUCTION,
            store_token=False
        )

    def get_authorization_url(self, redirect_uri, scope=DEFAULT_AUTH_SCOPE):
        return self.wepay.get_authorization_url(
            redirect_uri, WEPAY_CLIENT_ID, scope=scope
        )

    def service_create(self, owner, redirect_uri, code):
        # Get the OAuth token
        token_result = self.wepay.get_token(
            redirect_uri, WEPAY_CLIENT_ID,
            WEPAY_CLIENT_SECRET, code
        )
        if 'error' in token_result:
            return None

        # Get User Info
        user_result = self.wepay.call(
            '/user',
            token=token_result['access_token']
        )
        if 'error' in user_result:
            return None
        if user_result['state'] != 'registered':
            return None

        # Store details in database
        return self.db_service_create(
            owner, Service.SERVICE_WEPAY, token_result['user_id'],
            link_type=Service.LINK_TYPE_OAUTH, data={
                'access_token': token_result['access_token'],
                'token_type': token_result['token_type'],
                'email': user_result['email'],
                'user_name': user_result['user_name'],
                'first_name': user_result['first_name'],
                'last_name': user_result['last_name']
            }
        )

    def account_find(self, payee, name=None, reference_id=None):
        if not payee or not payee.user or not payee.user.valid():
            return None

        params = {}
        if name:
            params['name'] = name
        if reference_id:
            params['reference_id'] = reference_id

        return self.wepay.call(
            '/account/find', params,
            token=payee.user.data['access_token']
        )

    def donation_create(self, entity, recipient, payee,
                        amount, tip=0,
                        redirect_uri=None, callback_uri=None):
        amount = float(amount)
        tip = float(tip)
        if payee is None or payee.user is None:
            return None, None

        donation = self.db_donation_create(entity, recipient, payee,
                                           amount, tip=tip)

        # Create Transaction Short Description
        short_description = ""
        if tip > 0:
            short_description = string_length_limit(
                recipient.title, 127 - len(PaymentPlatform.DESC_FRUCTUS_TIP)
            ) + PaymentPlatform.DESC_FRUCTUS_TIP
        else:
            short_description = string_length_limit(recipient.title, 127)

        # Create Transaction Long Description
        long_description = ""
        if tip > 0:
            long_description = ", ".join([
                "%s Donation: $%.2f" % (recipient.title, amount),
                "Fruct.us Tip (Included in \"Fee\"): $%.2f" % tip,
                "Total Paid (Donation + Fruct.us Tip): $%.2f" % (amount + tip)
            ])
        else:
            long_description = ", ".join([
                "%s Donation: $%.2f" % (recipient.title, amount),
                "Total Paid: $%.2f" % amount
            ])

        params = {
            'account_id': payee.account_id,
            'short_description': short_description,
            'long_description': string_length_limit(long_description,
                                                    max_length=2047),
            'type': 'DONATION',
            'amount': amount + tip,
            'app_fee': tip,
            'fee_payer': 'Payee'
        }

        if redirect_uri:
            params['redirect_uri'] = redirect_uri

        if callback_uri:
            params['callback_uri'] = callback_uri

        create_result = self.wepay.call(
            '/checkout/create', params,
            token=payee.user.data['access_token']
        )

        if 'checkout_id' in create_result:
            donation.checkout_id = create_result['checkout_id']
            donation.save()

        if 'checkout_uri' in create_result:
            return donation, create_result['checkout_uri']
        else:
            return donation, None

    def donation_update(self, donation):
        result = self.wepay.call(
            '/checkout', {
                'checkout_id': donation.checkout_id
            },
            token=donation.payee.user.data['access_token']
        )

        if 'error' in result:
            return False

        donation.state = result['state']

        return True

wepay = WePayPaymentPlatform()
