from crispy_forms.bootstrap import FormActions, AppendedText, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Button, Layout, Fieldset, ButtonHolder, Submit, Field
from django import forms

__author__ = 'Dean Gardiner'


class WePayFindAccountForm(forms.Form):
    payee_id = forms.IntegerField(label="Payee ID")
    name = forms.CharField(required=False)
    reference_id = forms.CharField(label="Reference ID", required=False)

    # Crispy Forms Layout
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Fieldset('Find Account',
                 'payee_id',
                 'name',
                 'reference_id',
        ),
        FormActions(
            Submit('submit', 'Find', css_class='btn-primary')
        )
    )


class WePayCreateCheckoutForm(forms.Form):
    payee_id = forms.IntegerField(label="Payee ID")
    account_id = forms.IntegerField(label="Account ID")
    short_description = forms.CharField(max_length=127)
    type = forms.ChoiceField(
        choices=(
            ('GOODS', "Goods"),
            ('SERVICE', "Service"),
            ('DONATION', "Donation"),
            ('EVENT', "Event"),
            ('PERSONAL', "Personal")
        ),
    )
    amount = forms.DecimalField(decimal_places=2)

    # Extra Fields
    long_description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    payer_email_message = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    payee_email_message = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 3}))
    reference_id = forms.CharField(required=False)
    app_fee = forms.DecimalField(required=False, decimal_places=2)
    fee_payer = forms.ChoiceField(
        choices=(
            ('Payer', "Payer"),
            ('Payee', "Payee")
        )
    )

    # Crispy Forms Layout
    helper = FormHelper()
    helper.form_class = 'form-horizontal'
    helper.layout = Layout(
        Fieldset('Create Checkout',
                 'payee_id',
                 'account_id',
                 'short_description',
                 'type',
                 PrependedText('amount', '$'),
        ),
        Fieldset('Extra Fields',
            'long_description',
            'payer_email_message',
            'payee_email_message',
            'reference_id',
            PrependedText('app_fee', '$'),
            'fee_payer',
        ),
        FormActions(
            Submit('submit', 'Create', css_class='btn-primary')
        )
    )