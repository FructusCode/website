from __future__ import absolute_import
import braintree
from braintree.exceptions import AuthenticationError, NotFoundError
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, HTML
from django import forms
from django.conf import settings
from website.apwan.core.payment import PaymentPlatform, AUTHORIZATION_FORM, registry
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

    def __init__(self):
        PaymentPlatform.__init__(self)
        self.type = AUTHORIZATION_FORM
        self.form = BraintreeAuthorizationForm

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


if settings.FRUCTUS_KEYS:
    registry.register(BraintreePaymentPlatform())
