from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from wepay.exceptions import WePayError
from website.apwan.forms.account import PayeeSettingsForm, RecipientSettingsForm
from website.apwan.core.payment import wepay, PaymentPlatform
from website.apwan.models.payee import Payee
from website.apwan.models.recipient import Recipient
from website.apwan.models.service import Service
from website.settings import build_url

__author__ = 'Dean Gardiner'


ERRORS = {
    'INVALID_PAYEE': "<strong>Payee</strong> does not exist or access was denied",
    'INVALID_RECIPIENT': "<strong>Recipient</strong> does not exist or access was denied",
}


def error_redirect(error_key):
    return redirect(reverse('account-profile') + '?error=' + error_key)


def render_with_account_menu(template_name, request, dictionary=None):
    if dictionary is None:
        dictionary = {}

    dictionary['menu'] = {
        'payees': Payee.objects.all().filter(owner=request.user).order_by('title'),
        'recipients': Recipient.objects.all().filter(owner=request.user).order_by('s_title')
    }

    return render_to_response(template_name, context_instance=RequestContext(request, dictionary))


@login_required
def index(request):
    if 'error' in request.GET:
        if request.GET['error'] in ERRORS:
            return render_with_account_menu('account/index.html', request, {
                'error_key': request.GET['error'],
                'error_message': ERRORS[request.GET['error']]
            })
    return render_with_account_menu('account/index.html', request)

#
# Payee
#


@login_required
def payee_view(request, slug):
    payee = Payee.objects.filter(owner=request.user, slug=slug)
    if len(payee) != 1:
        return error_redirect('INVALID_PAYEE')
    payee = payee[0]

    return render_with_account_menu('account/payee/view.html', request, {
        'payee': payee.dict(),
    })


@login_required
def payee_settings(request, slug):
    payee = Payee.objects.filter(owner=request.user, slug=slug)
    if len(payee) != 1:
        return error_redirect('INVALID_PAYEE')
    payee = payee[0]

    if request.method == 'POST':
        form = PayeeSettingsForm(data=request.POST, payee=payee)
        if form.is_valid():
            payee.title = form.cleaned_data['title']
            payee.account_id = form.cleaned_data['account_id']
            payee.account_name = form.cleaned_data['account_name']
            payee.save()
            return redirect(reverse('account-payee-view', args=[payee.slug]))
    else:
        form = PayeeSettingsForm(payee=payee)

    return render_with_account_menu('account/form.html', request, {
        'form': form
    })


@login_required
def payee_add(request):
    error = None
    if request.method == 'POST':
        try:
            account_id = int(request.POST['account_id'])

            account = Service.objects.filter(owner=request.user, id=account_id)
            if len(account) == 1:
                account = account[0]

                PaymentPlatform.db_payee_create(account)
                return redirect(reverse('account-profile'))
            else:
                error = "Invalid Account ID"

        except ValueError:
            error = "Invalid Value"

    return render_with_account_menu('account/payee/add.html', request, {
        'error': error,
        'accounts': Service.objects.filter(owner=request.user, service_type=Service.TYPE_PAYEE_USER),
        'wepay': {
            'authorization_url': wepay.get_authorization_url(
                build_url(request, reverse('account-payee-add-wepay'))
            )
        }
    })


@login_required
def payee_add_wepay(request):
    if not 'code' in request.GET:
        return redirect(reverse('account-payee-add'))

    try:
        result = wepay.service_create(
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
        return error_redirect('INVALID_RECIPIENT')
    recipient = recipient[0]

    return render_with_account_menu('account/recipient/view.html', request, {
        'recipient': recipient.dict(payee_include=True),
    })


@login_required
def recipient_settings(request, slug):
    recipient = Recipient.objects.filter(owner=request.user, slug=slug)
    if len(recipient) != 1:
        return error_redirect('INVALID_RECIPIENT')
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