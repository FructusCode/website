from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from website import settings
from website.apwan.helpers.payment import wepay
from website.apwan.models.donation import Donation
from website.apwan.models.service import Service

__author__ = 'Dean Gardiner'


def index(request):
    pass


def complete(request, service):
    force = False
    if settings.DEBUG and 'force' in request.GET:
        force = True

    donation = Donation.objects.filter(checkout_id=request.GET['checkout_id'], payee__user__service=service)
    if len(donation) == 1:
        donation = donation[0]
    elif len(donation) > 1:
        return HttpResponse("Invalid Donation, Returned multiple donation objects")
    else:
        return HttpResponse("Invalid Donation, Unable to find donation")

    if donation.state == Donation.STATE_NEW or force:
        if donation.payee.user.service == Service.SERVICE_WEPAY:
            success = wepay.donation_update(donation)
            if success:
                donation.save()
                return HttpResponse("Donation Complete")
            else:
                return HttpResponse("Unable to update donation")
        else:
            return HttpResponse("Donation Service Not Implemented")
    else:
        if donation.state in [Donation.STATE_AUTHORIZED, Donation.STATE_RESERVED,
                              Donation.STATE_CAPTURED, Donation.STATE_SETTLED]:
            return HttpResponse("Donation Complete")
        else:
            return HttpResponse("Donation Service Failure: " + donation.get_state_display())