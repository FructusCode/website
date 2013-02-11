from django.http import HttpResponse
from website import settings
from website.apwan.core import payment
from website.apwan.models.donation import Donation

__author__ = 'Dean Gardiner'


def index(request):
    pass


def complete(request, service):
    force = False
    if settings.DEBUG and 'force' in request.GET:
        force = True
    return_message = None

    donation = Donation.objects.filter(checkout_id=request.GET['checkout_id'],
                                       payee__userservice__service=service)
    if len(donation) == 1:
        donation = donation[0]
    elif len(donation) > 1:
        return_message = "Invalid Donation, Returned multiple donation objects"
    else:
        return_message = "Invalid Donation, Unable to find donation"

    if return_message is not None:
        return HttpResponse(return_message)

    if donation.state == Donation.STATE_NEW or force:
        success = payment.registry[donation.payee.userservice.service].donation_update(donation)
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
