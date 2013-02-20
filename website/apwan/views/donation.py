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


def checkout(request, donation_id):
    # TODO: Replace donation_id with a random token
    donation = Donation.objects.filter(id=donation_id)

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
                                                      args=[donation_id]
                                                  )
                                              )
                                          )
                                      }))

    return HttpResponse("Invalid Donation Checkout")


def confirm(request, donation_id):
    # TODO: Replace donation_id with a random token
    donation = Donation.objects.filter(id=donation_id)

    if len(donation) == 1:
        donation = donation[0]
        platform = payment.registry[donation.payee.userservice.service]

        platform.donation_confirm(donation, request=request)

        return redirect('donation-complete', donation_id=donation.id)

    return HttpResponse('Invalid')


def complete(request, donation_id):
    # TODO: Replace donation_id with a random token

    force = False
    if settings.DEBUG and 'force' in request.GET:
        force = True
    return_message = None

    donation = Donation.objects.filter(id=donation_id)

    if len(donation) == 1:
        donation = donation[0]
        platform = payment.registry[donation.payee.userservice.service]

        if donation.state == Donation.STATE_NEW or force:
            success = platform.donation_update(donation)
            if success:
                donation.save()
                return_message = "Donation Complete"
            else:
                return_message = "Unable to update donation"
        else:
            if donation.state in [Donation.STATE_AUTHORIZED, Donation.STATE_RESERVED,
                                  Donation.STATE_CAPTURED, Donation.STATE_SETTLED]:
                return_message = "Donation Complete"
            else:
                return_message = "Donation Service Failure: " + \
                                 donation.get_state_display()

        return HttpResponse(return_message)

    return HttpResponse('Invalid')
