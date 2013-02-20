from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from website import settings
from website.apwan.core import payment
from website.apwan.models.donation import Donation
from website.settings import build_url

__author__ = 'Dean Gardiner'


def index(request):
    pass


def checkout(request, donation_token):
    donation = Donation.objects.filter(token=donation_token)

    if len(donation) == 1:
        donation = donation[0]
        platform = payment.registry[donation.payee.userservice.service]

        if platform.donation_type == payment.DONATION_INTERNAL:
            return render_to_response('donation/checkout.html',
                                      context_instance=RequestContext(request, {
                                          'form': platform.donation_form(
                                              donation,
                                              build_url(
                                                  request,
                                                  reverse(
                                                      'donation-confirm',
                                                      args=[donation_token]
                                                  )
                                              )
                                          )
                                      }))

    return HttpResponse("Invalid Donation Checkout")


def confirm(request, donation_token):
    donation = Donation.objects.filter(token=donation_token)

    if len(donation) == 1:
        donation = donation[0]
        platform = payment.registry[donation.payee.userservice.service]

        platform.donation_confirm(donation, request=request)

        return redirect('donation-complete', donation_token=donation_token)

    return HttpResponse('Invalid')


def complete(request, donation_token):
    force = False
    if settings.DEBUG and 'force' in request.GET:
        force = True
    return_message = ""

    donation = Donation.objects.filter(token=donation_token)

    if len(donation) == 1:
        donation = donation[0]
        platform = payment.registry[donation.payee.userservice.service]

        if donation.state == Donation.STATE_NEW or force:
            success = platform.donation_update(donation)
            if success:
                return_message = "Donation Updated<br/>"
            else:
                return_message = "Unable to update donation<br/>"

        if donation.state == Donation.STATE_AUTHORIZED:
            return_message += "Donation Authorized"
        elif donation.state == Donation.STATE_RESERVED:
            return_message += "Donation Reserved"
        elif donation.state == Donation.STATE_CAPTURED:
            return_message += "Donation Captured"
        elif donation.state == Donation.STATE_SETTLED:
            return_message += "Donation Settled"
        else:
            return_message += "Donation Service Failure: " + \
                             donation.get_state_display()

        return HttpResponse(return_message)

    return HttpResponse('Invalid')
