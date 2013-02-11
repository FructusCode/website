# pylint: disable=W0403
# pylint: disable=C0111
from django.core.urlresolvers import reverse

from django.db import IntegrityError
from website.apwan.models.donation import Donation
from website.apwan.models.payee import Payee
from website.apwan.models.service import Service
from website.settings import build_url

__author__ = 'Dean Gardiner'


AUTHORIZATION_AUTH = 'auth'
AUTHORIZATION_OAUTH = 'oauth'
AUTHORIZATION_ACCOUNT_ID = 'account_id'


class PaymentPlatform(object):
    DESC_FRUCTUS_TIP = " + Fruct.us Tip"

    def __init__(self):
        self.type = AUTHORIZATION_AUTH

    def get_oauth_url(self, redirect_uri, **kwargs):
        raise NotImplementedError()

    def service_create(self, owner, **kwargs):
        raise NotImplementedError()

    def account_find(self, payee, **kwargs):
        raise NotImplementedError()

    def donation_create(self, entity, recipient, payee,
                        amount, tip=0.0, **kwargs):
        raise NotImplementedError()

    def donation_update(self, donation):
        raise NotImplementedError()

    @staticmethod
    def db_payee_create(userservice, title="My Payee"):
        try:
            Payee.objects.create(
                owner=userservice.owner,
                userservice=userservice,
                title=title
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
            return True, Service.objects.create(
                owner=owner,

                service=service,
                service_id=service_id,
                service_type=Service.TYPE_PAYEE_USER,

                link_type=link_type,
                data=data
            )
        except IntegrityError:
            service = Service.objects.filter(
                owner=owner,

                service=service,
                service_id=service_id,
                service_type=Service.TYPE_PAYEE_USER,

                link_type=link_type
            )
            service.update(data=data)
            return False, service


class PaymentPlatformRegistry:
    def __init__(self):
        self.platforms = {}

    def build_info_dict(self, request=None):
        platforms = {}
        for pk, pv in self.platforms.items():
            p = {
                'title': pv.__platform_title__,
                'type': pv.type,
                'thumbnail': pv.__platform_thumbnail__,
                'description': pv.__platform_description__,
            }
            # Country
            if hasattr(pv, '__platform_country__'):
                p['country'] = pv.__platform_country__

            if hasattr(pv, '__platform_country_class__'):
                p['country_class'] = pv.__platform_country_class__

            # OAuth
            if pv.type == AUTHORIZATION_OAUTH:
                if request is None:
                    raise TypeError()
                p['oauth_url'] = pv.get_oauth_url(
                    build_url(request, reverse('account-payee-add-' + pk))
                )

            platforms[pk] = p
        return platforms

    def register(self, platform):
        if not isinstance(platform, PaymentPlatform):
            raise TypeError()
        if platform.__platform_key__ in self.platforms:
            print "platform already registered"
            return
        self.platforms[platform.__platform_key__] = platform
        print "'" + platform.__platform_key__ + "'", "payment platform registered"

    def __getitem__(self, key):
        return self.platforms[key]

    def __setitem__(self, key, value):
        raise Exception()

    def __contains__(self, key):
        return key in self.platforms

registry = PaymentPlatformRegistry()
