from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from wepay.exceptions import WePayError
from website.apwan.forms.account import PayeeSettingsForm, RecipientSettingsForm
from website.apwan.helpers.payment import wepay
from website.apwan.models.payee import Payee
from website.apwan.models.recipient import Recipient
from website.keys import WEPAY_CLIENT_ID
from website.settings import build_url

__author__ = 'Dean Gardiner'


def render_with_account_menu(template_name, request, dictionary=None):
    if dictionary is None:
        dictionary = {}

    dictionary['menu'] = {
        'payees': Payee.objects.all().filter(owner=request.user).order_by('name'),
        'recipients': Recipient.objects.all().filter(owner=request.user).order_by('title')
    }

    return render_to_response(template_name, context_instance=RequestContext(request, dictionary))


@login_required
def index(request):
    return render_with_account_menu('account/index.html', request)

#
# Payee
#


@login_required
def payee_view(request, slug):
    payee = Payee.objects.filter(owner=request.user, slug=slug)
    if len(payee) != 1:
        return redirect(reverse('account-profile'))  # TODO: Maybe we should redirect to an error page?
    payee = payee[0]

    return render_with_account_menu('account/payee/view.html', request, {
        'payee': payee.dict(),
    })


@login_required
def payee_settings(request, slug):
    payee = Payee.objects.filter(owner=request.user, slug=slug)
    if len(payee) != 1:
        return redirect(reverse('account-profile'))  # TODO: Maybe we should redirect to an error page?
    payee = payee[0]

    if request.method == 'POST':
        form = PayeeSettingsForm(data=request.POST, payee=payee)
        if form.is_valid():
            payee.name = form.cleaned_data['name']
            payee.account_id = form.cleaned_data['account_id']
            payee.save()
            return redirect(reverse('account-payee-view', args=[payee.slug]))
    else:
        form = PayeeSettingsForm(payee=payee)

    return render_with_account_menu('account/form.html', request, {
        'form': form
    })


@login_required
def payee_add(request):
    return render_with_account_menu('account/payee/add.html', request, {
        'wepay': {
            'authorization_url': wepay.get_authorization_url(
                build_url(request, reverse('account-payee-add-wepay'))
            )
        }
    })


@login_required
def payee_add_wepay(request):
    if not 'code' in request.GET:
        return redirect('/account/payee/add')

    try:
        result = wepay.store_token(
            request.user,
            build_url(request, reverse('account-payee-add-wepay')),
            request.GET['code']
        )
        if result:
            return redirect(reverse('account-profile'))
        else:
            print 'error storing token (already exists?)'
    except WePayError, e:
        print e
        if e.type == 'access_denied':
            return redirect(wepay.get_authorization_url(
                build_url(request, reverse('account-payee-add-wepay'))
            ))

    return HttpResponse()

#
# Recipient
#


@login_required
def recipient_claim(request):
    return render_with_account_menu('account/recipient/claim.html', request)


@login_required
def recipient_view(request, slug):
    recipient = Recipient.objects.filter(owner=request.user, slug=slug)
    if len(recipient) != 1:
        return redirect(reverse('account-profile'))  # TODO: Maybe we should redirect to an error page?
    recipient = recipient[0]

    return render_with_account_menu('account/recipient/view.html', request, {
        'recipient': recipient.dict(payee_include=True),
    })


@login_required
def recipient_settings(request, slug):
    recipient = Recipient.objects.filter(owner=request.user, slug=slug)
    if len(recipient) != 1:
        return redirect(reverse('account-profile'))  # TODO: Maybe we should redirect to an error page?
    recipient = recipient[0]

    payee_choices = Payee.objects.filter(owner=request.user)

    if request.method == 'POST':
        form = RecipientSettingsForm(data=request.POST, recipient=recipient, payee_choices=payee_choices)
        if form.is_valid():
            recipient.payee = payee_choices.filter(id=form.cleaned_data['payee_id'])[0]
            recipient.save()
            return redirect(reverse('account-recipient-view', args=[recipient.slug]))
    else:
        form = RecipientSettingsForm(recipient=recipient, payee_choices=payee_choices)

    return render_with_account_menu('account/form.html', request, {
        'form': form
    })

#
# Report
#


@login_required
def report_donations(request):
    return render_with_account_menu('account/report/donations.html', request)