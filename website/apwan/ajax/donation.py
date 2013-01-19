from dajaxice.decorators import dajaxice_register
from django.utils import simplejson

__author__ = 'Dean Gardiner'


@dajaxice_register(method='GET', name='donation.checkout')
def checkout(request, recipient_id, entity_id, amount):
    print recipient_id, entity_id, amount
    return simplejson.dumps({})