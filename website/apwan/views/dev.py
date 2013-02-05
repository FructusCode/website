from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from website.apwan.forms.dev import WePayCreateCheckoutForm, WePayFindAccountForm
from website.apwan.helpers.payment import wepay
from website.apwan.models.payee import Payee

__author__ = 'Dean Gardiner'


@login_required(login_url='/account/login/')
def index(request):
    return render_to_response('dev/index.html',
                              context_instance=RequestContext(request, {}))


#
# Entity
#


@login_required(login_url='/account/login/')
def entity_search(request):
    return render_to_response('dev/entity/search.html',
                              context_instance=RequestContext(request, {}))

#
# Donation
#


@login_required(login_url='/account/login/')
def donation_create(request):
    return render_to_response('dev/donation/create.html',
                              context_instance=RequestContext(request, {}))


#
# WePay
#


@login_required(login_url='/account/login/')
def wepay_account_find(request):
    results = None
    if request.method == 'POST':
        form = WePayFindAccountForm(request.POST)
        if form.is_valid():
            payee = Payee.objects.get(pk=form.cleaned_data['payee_id'])
            results = wepay.wepay.call(
                '/account/find', {
                    'name':         form.cleaned_data['name'],
                    'reference_id': form.cleaned_data['reference_id'],
                },
                token=str(payee.token)
            )
    else:
        form = WePayFindAccountForm()

    return render_to_response('dev/wepay/account/find.html',
                              context_instance=RequestContext(request, {
                                  'form': form,
                                  'results': results
                              }))


@login_required(login_url='/account/login/')
def wepay_checkout_create(request):
    result = None
    if request.method == 'POST':
        form = WePayCreateCheckoutForm(request.POST)
        if form.is_valid():
            payee = Payee.objects.get(pk=form.cleaned_data['payee_id'])
            result = wepay.wepay.call(
                '/checkout/create', {
                    'account_id':           str(form.cleaned_data['account_id']),
                    'short_description':    form.cleaned_data['short_description'],
                    'type':                 form.cleaned_data['type'],
                    'amount':               str(form.cleaned_data['amount']),

                    # Extra Fields
                    'long_description':     form.cleaned_data['long_description'],
                    'payer_email_message':  form.cleaned_data['payer_email_message'],
                    'payee_email_message':  form.cleaned_data['payee_email_message'],
                    'reference_id':         form.cleaned_data['reference_id'],
                    'app_fee':              str(form.cleaned_data['app_fee']),
                    'fee_payer':            form.cleaned_data['fee_payer'],
                },
                token=str(payee.token)
            )
    else:
        form = WePayCreateCheckoutForm()

    return render_to_response('dev/wepay/checkout/create.html',
                              context_instance=RequestContext(request, {
                                  'form': form,
                                  'result': result
                              }))