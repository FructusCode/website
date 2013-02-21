# pylint: disable=E0611
# pylint: disable=F0401
from __future__ import absolute_import
# noinspection PyUnresolvedReferences
from django.conf import settings
from django.core.urlresolvers import reverse
from wepay import WePay
from website.apwan.core import string_length_limit
from website.apwan.core.payment import (PaymentPlatform, registry, PaymentPlatformMeta,
                                        AUTHORIZATION_OAUTH, DONATION_REDIRECT)
from website.apwan.models.service import Service
# pylint: enable=E0611
# pylint: enable=F0401

__author__ = 'Dean Gardiner'


class WePayPaymentPlatform(PaymentPlatform):
    class Meta(PaymentPlatformMeta):
        key = Service.SERVICE_WEPAY
        title = "WePay"
        thumbnail = "/img/media/wepay.png"
        description = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                         Vivamus placerat venenatis libero vel pellentesque."""

        authorization_type = AUTHORIZATION_OAUTH
        donation_type = DONATION_REDIRECT

        country = "United States"
        country_class = "label-info"

    DEFAULT_AUTH_SCOPE = "manage_accounts,collect_payments,view_user"

    def __init__(self):
        PaymentPlatform.__init__(self)

        self.wepay = WePay(
            production=settings.FRUCTUS_KEYS.WEPAY_PRODUCTION,
            store_token=False
        )

    def get_oauth_url(self, redirect_uri, **kwargs):
        _scope = self.DEFAULT_AUTH_SCOPE
        if 'scope' in kwargs:
            _scope = kwargs['scope']

        return self.wepay.get_authorization_url(
            redirect_uri, settings.FRUCTUS_KEYS.WEPAY_CLIENT_ID, scope=_scope
        )

    def service_create(self, owner, **kwargs):
        if 'code' not in kwargs:
            raise TypeError()
        if 'redirect_uri' not in kwargs:
            raise TypeError()

        # Get the OAuth token
        token_result = self.wepay.get_token(
            kwargs['redirect_uri'], settings.FRUCTUS_KEYS.WEPAY_CLIENT_ID,
            settings.FRUCTUS_KEYS.WEPAY_CLIENT_SECRET, kwargs['code']
        )
        if 'error' in token_result:
            return False, None

        # Get User Info
        user_result = self.wepay.call(
            '/user',
            token=token_result['access_token']
        )
        if 'error' in user_result:
            return False, None
        if user_result['state'] != 'registered':
            return False, None

        # Store details in database
        return self.db_service_create(
            owner, Service.SERVICE_WEPAY, token_result['user_id'],
            link_type=Service.LINK_TYPE_OAUTH, data={
                'access_token': token_result['access_token'],
                'token_type': token_result['token_type'],
                'email': user_result['email'],
                'name': user_result['user_name'],
                'first_name': user_result['first_name'],
                'last_name': user_result['last_name']
            }
        )

    def account_find(self, payee, **kwargs):
        if not payee or not payee.userservice or not payee.userservice.valid():
            return None

        params = {}
        if 'name' in kwargs:
            params['name'] = kwargs['name']
        if 'reference_id' in kwargs:
            params['reference_id'] = kwargs['reference_id']

        return self.wepay.call(
            '/account/find', params,
            token=payee.userservice.data['access_token']
        )

    def donation_create(self, entity, recipient, payee,
                        amount, tip=0.0, **kwargs):
        amount = float(amount)
        tip = float(tip)
        if payee is None or payee.userservice is None:
            return None, None

        donation = self.db_donation_create(entity, recipient, payee,
                                           amount, tip=tip)

        # Create donation descriptions
        short_description = self.short_description(recipient, tip)
        long_description = self.long_description(recipient, amount, tip)

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

        # TODO: this could do with a cleanup
        if 'base_url' in kwargs:
            if 'redirect_name' in kwargs:
                params['redirect_uri'] = kwargs['base_url'] + reverse(
                    kwargs['redirect_name'],
                    args=[donation.token]
                )

            if 'callback_name' in kwargs:
                params['callback_uri'] = kwargs['base_url'] + reverse(
                    kwargs['callback_name']
                )

        create_result = self.wepay.call(
            '/checkout/create', params,
            token=payee.userservice.data['access_token']
        )

        if 'checkout_id' in create_result:
            donation.checkout_id = create_result['checkout_id']
            donation.save()

        if 'checkout_uri' in create_result:
            return donation, create_result['checkout_uri']
        else:
            return donation, None

    def donation_confirm(self, donation, **kwargs):
        pass

    def donation_update(self, donation):
        result = self.wepay.call(
            '/checkout', {
                'checkout_id': donation.checkout_id
            },
            token=donation.payee.userservice.data['access_token']
        )

        if 'error' in result:
            return False

        donation.state = result['state']
        donation.save()

        return True

if settings.FRUCTUS_KEYS:  # Only register if website.keys is available.
    registry.register(WePayPaymentPlatform())
