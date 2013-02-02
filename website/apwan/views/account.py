from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from wepay.exceptions import WePayError
from website.apwan.forms.account import EditPayeeForm
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


@login_required(login_url='/account/login/')
def index(request):
    return render_with_account_menu('account/index.html', request)


@login_required(login_url='/account/login/')
def payee_view(request, slug):
    payee = Payee.objects.filter(owner=request.user, slug=slug)
    if len(payee) != 1:
        return redirect('/account/profile')  # TODO: Maybe we should redirect to an error page?
    payee = payee[0]

    return render_with_account_menu('account/payee/view.html', request, {
        'payee': payee.dict(),
    })


@login_required(login_url='/account/login/')
def payee_edit(request, slug):
    payee = Payee.objects.filter(owner=request.user, slug=slug)
    if len(payee) != 1:
        return redirect('/account/profile')  # TODO: Maybe we should redirect to an error page?
    payee = payee[0]

    if request.method == 'POST':
        form = EditPayeeForm(data=request.POST, payee=payee)
        if form.is_valid():
            payee.name = form.cleaned_data['name']
            payee.account_id = form.cleaned_data['account_id']
            payee.save()
            return redirect('/account/payee/%s' % payee.slug)
    else:
        form = EditPayeeForm(payee=payee)

    return render_with_account_menu('account/payee/edit.html', request, {
        'form': form
    })


@login_required(login_url='/account/login/')
def payee_add(request):
    return render_with_account_menu('account/payee/add.html', request, {
        'wepay': {
            'authorization_url': wepay.get_authorization_url(
                build_url(request, '/account/payee/add/wepay/')
            )
        }
    })


@login_required(login_url='/account/login/')
def payee_add_wepay(request):
    if not 'code' in request.GET:
        return redirect('/account/payee/add')

    try:
        result = wepay.store_token(
            request.user,
            build_url(request, '/account/payee/add/wepay/'),
            request.GET['code']
        )
        if result:
            return redirect('/account/')
        else:
            print 'error storing token (already exists?)'
    except WePayError, e:
        print e
        if e.type == 'access_denied':
            return redirect(wepay.get_authorization_url(
                build_url(request, '/account/payee/add/wepay/')
            ))

    return HttpResponse()


@login_required(login_url='/account/login/')
def recipient_claim(request):
    return render_with_account_menu('account/recipient/claim.html', request)


@login_required(login_url='/account/login/')
def report_donations(request):
    return render_with_account_menu('account/report/donations.html', request)