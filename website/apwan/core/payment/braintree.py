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

    def service_create(self, owner, **kwargs):
        if 'public_key' not in kwargs:
            raise TypeError()
        if 'private_key' not in kwargs:
            raise TypeError()
        if 'merchant_id' not in kwargs:
            raise TypeError()

        print 'service_create'


class BraintreeAuthorizationForm(forms.Form):
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
