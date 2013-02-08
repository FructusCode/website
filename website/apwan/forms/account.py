from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Layout, HTML
from django import forms
from website.apwan.core.payment import wepay

__author__ = 'Dean Gardiner'


class PayeeSettingsForm(forms.Form):
    title = forms.CharField(label="Title")
    account_id = forms.ChoiceField(label="Account")

    def __init__(self, data=None, payee=None, *args, **kwargs):
        # Crispy Forms Layout
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('Payee Settings',
                     'title',
                     'account_id'
            ),
            FormActions(
                Submit('submit', 'Save Changes', css_class='btn-primary'),
                HTML('<a class="btn" href="/account/payee/%s">Cancel</a>'
                     % payee.slug)
            )
        )
        super(PayeeSettingsForm, self).__init__(data=data, initial={
            'title': payee.title,
            'account_id': payee.account_id
        })

        if payee:
            if not data or data['account_id'] != payee.account_id:
                account_choices = []
                for account in wepay.account_find(payee):
                    account_choices.append(
                        (account['account_id'], account['name']))
                self.fields['account_id'].choices = tuple(account_choices)

    def clean(self):
        cleaned_data = super(PayeeSettingsForm, self).clean()

        cleaned_data['account_name'] = None
        for account_id, account_name in self.fields['account_id'].choices:
            if str(account_id) == str(cleaned_data['account_id']):
                cleaned_data['account_name'] = account_name

        return cleaned_data


class RecipientSettingsForm(forms.Form):
    payee_id = forms.ChoiceField(label="Payee")

    def __init__(self, data=None, recipient=None, payee_choices=None,
                 *args, **kwargs):
        # Crispy Forms Layout
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('Recipient Settings',
                     'payee_id'
            ),
            FormActions(
                Submit('submit', 'Save Changes', css_class='btn-primary'),
                HTML('<a class="btn" href="/account/recipient/%s">Cancel</a>'
                     % recipient.slug)
            )
        )
        recipient_payee_id = None
        if recipient.payee:
            recipient_payee_id = recipient.payee.id
        super(RecipientSettingsForm, self).__init__(data=data, initial={
            'payee_id': recipient_payee_id
        })

        if payee_choices:
            if not data or data['payee_id'] != recipient_payee_id:
                payee_field_choices = []
                for payee in payee_choices:
                    payee_field_choices.append((payee.id, payee.title))
                self.fields['payee_id'].choices = tuple(payee_field_choices)
