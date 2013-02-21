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

        if donation.state == Donation.STATE_EXPIRED:
            return HttpResponse('Donation has expired')
        elif donation.state != Donation.STATE_NEW:
            return HttpResponse('Donation has already been processed')

        platform = payment.registry[donation.payee.userservice.service]

        # Only accept platforms with DONATION_FORM as 'donation_type'
        if (platform.Meta.donation_type == payment.DONATION_FORM and
                platform.Meta.donation_form is not None):

            return render_to_response('donation/checkout.html',
                                      context_instance=RequestContext(request, {
                                          'form': platform.Meta.donation_form(
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
        else:
            return HttpResponse("Payment Platform doesn't require hosted checkouts")
    else:
        return HttpResponse("Unable to find your donation")


def confirm(request, donation_token):
    donation = Donation.objects.filter(token=donation_token)

    if len(donation) == 1:
        donation = donation[0]

        if donation.state == Donation.STATE_EXPIRED:
            return HttpResponse('Donation has expired')
        elif donation.state != Donation.STATE_AUTHORIZED:
            return HttpResponse('Donation has already been processed')

        platform = payment.registry[donation.payee.userservice.service]

        # Checking if form has been confirmed
        confirmed = request.POST and 'submit' in request.POST

        # Only accept platforms with DONATION_CONFIRMATION_FORM as 'confirmation_type'
        if (platform.Meta.confirmation_type == payment.DONATION_CONFIRMATION_FORM and
                platform.Meta.confirmation_form is not None):

            if confirmed:
                # User has confirmed the transaction, continue donation process.
                platform.donation_confirm(donation, request=request)
                return redirect('donation-complete', donation_token=donation_token)
            else:
                # Present the payment platform confirmation form
                return render_to_response('donation/confirm.html',
                                          context_instance=RequestContext(request, {
                                              'form': platform.donation_confirm_form(
                                                  donation
                                              )
                                          }))
        else:
            return HttpResponse("Payment Platform doesn't require hosted confirmations")
    else:
        return HttpResponse('Unable to find your donation')


def complete(request, donation_token):
    force = False
    if settings.DEBUG and 'force' in request.GET:
        force = True
    return_message = ""

    donation = Donation.objects.filter(token=donation_token)

    if len(donation) == 1:
        donation = donation[0]

        platform = payment.registry[donation.payee.userservice.service]

        # Update the donation status (and handle 'force' GET parameter)
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
            return_message += "Donation Service Failure: " + donation.get_state_display()

        return HttpResponse(return_message)

    return HttpResponse('Invalid')
