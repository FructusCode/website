from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from wepay.exceptions import WePayError
from website.apwan.core import payment
from website.apwan.forms.account import PayeeSettingsForm, RecipientSettingsForm
from website.apwan.models.payee import Payee
from website.apwan.models.recipient import Recipient
from website.apwan.models.service import Service
from website.settings import build_url

__author__ = 'Dean Gardiner'


ERRORS = {
    'INVALID_PAYEE': "<strong>Payee</strong> does not exist or access was denied",
    'INVALID_RECIPIENT': "<strong>Recipient</strong> does not exist or access was denied",
    'ALREADY_AUTHORIZED': "<strong>Account</strong> already authorized",
    'UNKNOWN_AUTHORIZATION_ERROR': "Unknown authorization error",
}


def error_redirect(error_key):
    return redirect(reverse('account-profile') + '?error=' + error_key)


def render_with_account_menu(template_name, request, dictionary=None):
    if dictionary is None:
        dictionary = {}

    dictionary['menu'] = {
        'payees': Payee.objects.all().filter(
            owner=request.user
        ).order_by('title'),

        'recipients': Recipient.objects.all().filter(
            owner=request.user
        ).order_by('s_title')
    }

    return render_to_response(
        template_name, context_instance=RequestContext(request, dictionary))


@login_required
def index(request):
    dictionary = {}

    if 'error' in request.GET:
        if request.GET['error'] in ERRORS:
            dictionary['error_key'] = request.GET['error']
            dictionary['error_message'] = ERRORS[request.GET['error']]

    return render_with_account_menu('account/index.html', request, dictionary)

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

            userservice = Service.objects.filter(owner=request.user, id=account_id)
            if len(userservice) == 1:
                userservice = userservice[0]

                payment.PaymentPlatform.db_payee_create(userservice)
                return redirect(reverse('account-profile'))
            else:
                error = "Invalid User Service ID"

        except ValueError:
            error = "Invalid Value"

    return render_with_account_menu('account/payee/add.html', request, {
        'error': error,
        'accounts': Service.objects.filter(
            owner=request.user, service_type=Service.TYPE_PAYEE_USER
        ),
        'platforms': payment.registry.build_info_dict(request)
    })


@login_required
def payee_add_wepay(request):
    if not 'code' in request.GET:
        return redirect(reverse('account-payee-add'))

    try:
        created, service = payment.registry[Service.SERVICE_WEPAY].service_create(
            request.user,
            redirect_uri=build_url(request, reverse('account-payee-add-wepay')),
            code=request.GET['code']
        )
        if service:
            if created:
                return redirect(reverse('account-profile'))
            else:
                return error_redirect('ALREADY_AUTHORIZED')
        else:
            return error_redirect('UNKNOWN_AUTHORIZATION_ERROR')
    except WePayError, e:
        print e
        if e.type == 'access_denied':
            return redirect(payment.registry[Service.SERVICE_WEPAY].get_oauth_url(
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
        form = RecipientSettingsForm(data=request.POST, recipient=recipient,
                                     payee_choices=payee_choices)
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
