# pylint: disable=R0924

from __future__ import absolute_import
import braintree
from braintree.exceptions import AuthenticationError, NotFoundError
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from website.apwan.core.payment import PaymentPlatform, AUTHORIZATION_FORM, registry, DONATION_INTERNAL
from website.apwan.models.donation import Donation
from website.apwan.models.service import Service

__author__ = 'Dean Gardiner'


class BraintreePaymentPlatform(PaymentPlatform):
    __platform_key__ = Service.SERVICE_BRAINTREE
    __platform_title__ = "Braintree"
    __platform_thumbnail__ = "/img/media/braintree.png"
    __platform_description__ = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    Vivamus placerat venenatis libero vel pellentesque.
    """

    __platform_country__ = "Australia, Europe, Canada"
    __platform_country_class__ = "label-info"

    BRAINTREE_STATE_MAP = {
        'authorized': Donation.STATE_AUTHORIZED,
        'processor_declined': Donation.STATE_FAILED,
        'gateway_rejected': Donation.STATE_FAILED,
        'failed': Donation.STATE_FAILED,
        'voided': Donation.STATE_CANCELLED,
        'submitted_for_settlement': Donation.STATE_CAPTURED,
        'settled': Donation.STATE_SETTLED,
        'settling': Donation.STATE_CAPTURED,
        'authorization_expired': Donation.STATE_EXPIRED
    }

    def __init__(self):
        PaymentPlatform.__init__(self)
        self.type = AUTHORIZATION_FORM
        self.form = BraintreeAuthorizationForm

        self.donation_type = DONATION_INTERNAL
        self.donation_form = BraintreeDonationForm

        self.donation_confirm_form = BraintreeDonationConfirmationForm

        self.configure(None, None, None)  # Initial blank configuration

    @staticmethod
    def configure(merchant_id, public_key, private_key):
        environment = braintree.Environment.Production
        if not settings.FRUCTUS_KEYS.BRAINTREE_PRODUCTION:
            environment = braintree.Environment.Sandbox

        braintree.Configuration.configure(
            environment, merchant_id,
            public_key, private_key,
            use_once=True
        )

    @staticmethod
    def configure_payee(payee):
        if payee.userservice.service == Service.SERVICE_BRAINTREE:
            BraintreePaymentPlatform.configure(
                payee.userservice.service_id,
                payee.userservice.data['public_key'],
                payee.userservice.data['private_key']
            )
        else:
            raise ValueError()

    @staticmethod
    def from_transaction_status(status):
        return BraintreePaymentPlatform.BRAINTREE_STATE_MAP.get(status)

    @staticmethod
    def to_transaction_status(state):
        for key, value in BraintreePaymentPlatform.BRAINTREE_STATE_MAP.items():
            if value == state:
                return key
        raise KeyError()

    def service_create(self, owner, **kwargs):
        if 'public_key' not in kwargs:
            raise TypeError()
        if 'private_key' not in kwargs:
            raise TypeError()
        if 'merchant_id' not in kwargs:
            raise TypeError()

        self.configure(kwargs['merchant_id'],
                       kwargs['public_key'],
                       kwargs['private_key'])

        # Check if details are correct
        # TODO: Surely there is a better way to do this?
        try:
            braintree.Transaction.find('fructus-account-validation-check')
            account_valid = True
        except AuthenticationError:
            account_valid = False
        except NotFoundError:
            account_valid = True

        if not account_valid:
            return False, None  # (created, service)

       # Store details in database
        return self.db_service_create(
            owner, Service.SERVICE_BRAINTREE, kwargs['merchant_id'],
            link_type=Service.LINK_TYPE_KEY, data={
                'public_key': kwargs['public_key'],
                'private_key': kwargs['private_key'],
                'name': kwargs.get('name', '')
            }
        )

    def account_find(self, payee, **kwargs):
        # Braintree authorizations only have access to a single account
        return [
            {
                'account_id': payee.userservice.service_id,
                'name': payee.userservice.name()
            }
        ]

    def donation_create(self, entity, recipient, payee,
                        amount, tip=0.0, **kwargs):
        amount = float(amount)

        tip = float(tip)
        if tip != 0.0:
            raise ValueError()  # Tips aren't supported with braintree

        if payee is None or payee.userservice is None:
            return None, None

        donation = self.db_donation_create(entity, recipient, payee,
                                           amount, tip=0.0)

        # Passing onto our donation checkout page
        return donation, reverse('donation-checkout', args=[donation.token])

    def donation_confirm(self, donation, **kwargs):
        if not 'request' in kwargs:
            raise TypeError()

        self.configure_payee(donation.payee)

        result = braintree.TransparentRedirect.confirm(
            kwargs['request'].META['QUERY_STRING']
        )

        if 'id' in kwargs['request'].GET:
            donation.checkout_id = result.transaction.id

        donation.state = self.from_transaction_status(result.transaction.status)
        donation.save()

    def donation_update(self, donation):
        self.configure_payee(donation.payee)
        result = braintree.Transaction.find(donation.checkout_id)

        donation.state = self.from_transaction_status(result.status)
        donation.save()

        return True


class BraintreeAuthorizationForm(forms.Form):
    name = forms.CharField(label='Name', required=False,
                           help_text='To help you find the account later')
    merchant_id = forms.CharField(label="Merchant ID")
    public_key = forms.CharField(label="Public Key")
    private_key = forms.CharField(label="Private Key")

    def __init__(self, *args, **kwargs):
        # Crispy Forms Layout
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Link Braintree Account',
                'name',
                'merchant_id',
                'public_key',
                'private_key'
            ),
            FormActions(
                Submit('submit', 'Link', css_class='btn-primary'),
                HTML('<a class="btn" href="/account/add_payee">Cancel</a>')
            )
        )

        super(BraintreeAuthorizationForm, self).__init__(*args, **kwargs)


class BraintreeDonationForm(forms.Form):
    transaction__credit_card__cardholder_name = forms.CharField()
    transaction__credit_card__number = forms.CharField()
    transaction__credit_card__expiration_month = forms.IntegerField()
    transaction__credit_card__expiration_year = forms.IntegerField()
    transaction__credit_card__cvv = forms.IntegerField()

    tr_data = forms.CharField()

    def __init__(self, donation, redirect_url, *args, **kwargs):
        BraintreePaymentPlatform.configure_payee(donation.payee)

        # Crispy Forms Layout
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_action = braintree.TransparentRedirect.url()
        self.helper.layout = Layout(
            Fieldset(
                'Donation for ' + BraintreePaymentPlatform.short_description(
                    donation.recipient
                ),
                'transaction__credit_card__cardholder_name',
                'transaction__credit_card__number',
                'transaction__credit_card__expiration_month',
                'transaction__credit_card__expiration_year',
                'transaction__credit_card__cvv',

                'tr_data'
            ),
            FormActions(
                Submit('submit', 'Donate', css_class='btn-primary'),
                HTML('<a class="btn" href="/">Cancel</a>')
            )
        )

        super(BraintreeDonationForm, self).__init__(*args, **kwargs)

        # Add tr_data to form
        BraintreePaymentPlatform.configure_payee(donation.payee)
        self.fields['tr_data'].initial = braintree.Transaction.tr_data_for_sale(
            {
                'transaction': {
                    'amount': str(donation.amount),
                    'order_id': str(donation.token),
                    'options': {
                        'submit_for_settlement': True
                    }
                }
            }, redirect_url
        )
        self.fields['tr_data'].widget = forms.HiddenInput()


class BraintreeDonationConfirmationForm(forms.Form):
    def __init__(self, donation, *args, **kwargs):
        # Crispy Forms Layout
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset(
                'Confirm Donation for ' + BraintreePaymentPlatform.short_description(
                    donation.recipient
                ),
            ),
            FormActions(
                Submit('submit', 'Confirm Donation'),
                HTML('<a class="btn" href="/">Cancel</a>')
            )
        )

        super(BraintreeDonationConfirmationForm, self).__init__(*args, **kwargs)


if settings.FRUCTUS_KEYS:
    registry.register(BraintreePaymentPlatform())
