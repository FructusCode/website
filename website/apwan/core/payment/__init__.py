# pylint: disable=W0403
# pylint: disable=C0111
import inspect
from django.core.urlresolvers import reverse

from django.db import IntegrityError
from website.apwan.core import string_length_limit
from website.apwan.models.donation import Donation
from website.apwan.models.payee import Payee
from website.apwan.models.service import Service
from website.settings import build_url


AUTHORIZATION_AUTH = 'auth'
AUTHORIZATION_OAUTH = 'oauth'
AUTHORIZATION_FORM = 'form'

DONATION_REDIRECT = 'redirect'
DONATION_FORM = 'form'

CONFIRMATION_NONE = 'none'
CONFIRMATION_FORM = 'form'


class PaymentPlatformMeta:
    key = None
    title = ""
    thumbnail = ""
    description = ""

    authorization_type = ''
    authorization_form = None

    donation_type = ''
    donation_form = None

    confirmation_type = CONFIRMATION_NONE
    confirmation_form = None

    country = ""
    country_class = ""


class PaymentPlatform:
    class Meta(PaymentPlatformMeta):
        pass

    DESC_FRUCTUS_TIP = " + Fruct.us Tip"

    def __init__(self):
        pass

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

    @staticmethod
    def short_description(recipient, tip=0.0):
        if tip > 0:
            return string_length_limit(
                recipient.title, 127 - len(PaymentPlatform.DESC_FRUCTUS_TIP)
            ) + PaymentPlatform.DESC_FRUCTUS_TIP
        else:
            return string_length_limit(recipient.title, 127)

    @staticmethod
    def long_description(recipient, amount, tip=0.0):
        if tip > 0:
            return ", ".join([
                "%s Donation: $%.2f" % (recipient.title, amount),
                "Fruct.us Tip (Included in \"Fee\"): $%.2f" % tip,
                "Total Paid (Donation%s): $%.2f" % (
                    PaymentPlatform.DESC_FRUCTUS_TIP, amount + tip
                )
            ])
        else:
            return ", ".join([
                "%s Donation: $%.2f" % (recipient.title, amount),
                "Total Paid: $%.2f" % amount
            ])


class PaymentPlatformRegistry:
    def __init__(self):
        self.platforms = {}

    def build_info_dict(self, request=None):
        platforms = {}
        for key, platform in self.platforms.items():
            if isinstance(platform, PaymentPlatform):
                # Build a dictionary of the platform Meta
                platform_info = {}
                for attr_key, attr_value in platform.Meta.__dict__.items():
                    if not attr_key.startswith('__') and not attr_key.endswith('__'):
                        platform_info[attr_key] = attr_value

                # Build the OAuth url if the platform uses OAuth
                if platform.Meta.authorization_type == AUTHORIZATION_OAUTH:
                    if request is None:
                        raise TypeError()
                    platform_info['oauth_url'] = platform.get_oauth_url(
                        build_url(request, reverse('account-payee-add-' + key))
                    )

                platforms[key] = platform_info
        return platforms

    def register(self, platform):
        if isinstance(platform, PaymentPlatform):
            if platform.Meta.key in self.platforms:
                print "platform already registered"
                return
            self.platforms[platform.Meta.key] = platform
        else:
            print platform.Meta.key, "is not a valid payment platform"

    def __getitem__(self, key):
        return self.platforms[key]

    def __setitem__(self, key, value):
        raise Exception()

    def __delitem__(self, key):
        raise Exception()

    def __contains__(self, key):
        return key in self.platforms

    def __len__(self):
        return len(self.platforms)


registry = PaymentPlatformRegistry()
