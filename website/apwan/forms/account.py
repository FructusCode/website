from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Fieldset, Layout, Button, Field, HTML
from django import forms
from website.apwan.helpers.payment import wepay

__author__ = 'Dean Gardiner'


class EditPayeeForm(forms.Form):
    name = forms.CharField(label="Name")
    account_id = forms.ChoiceField(label="Account")

    def __init__(self, data=None, payee=None, *args, **kwargs):
        # Crispy Forms Layout
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.layout = Layout(
            Fieldset('Edit Payee',
                     'name',
                     'account_id'
            ),
            FormActions(
                Submit('submit', 'Save Changes', css_class='btn-primary'),
                HTML('<a class="btn" href="/account/payee/%s">Cancel</a>' % payee.slug)
            )
        )
        super(EditPayeeForm, self).__init__(data=data, initial={
            'name': payee.name,
            'account_id': payee.account_id
        })

        if payee:
            if not data or data['account_id'] != payee.account_id:
                account_choices = []
                self.account_map = {}
                for account in wepay.account_find(payee):
                    account_choices.append((account['account_id'], account['name']))
                    self.account_map[account['account_id']] = account['name']
                self.fields['account_id'].choices = tuple(account_choices)