from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from website.apwan.ajax.utils import cors_response
from website.apwan.models.entity import Entity

__author__ = 'Dean Gardiner'


@dajaxice_register(method='GET', name='donation.checkout')
def checkout(request, recipient_id, entity_id, amount):
    # Get entity
    entity = Entity.objects.filter(pk=entity_id)
    if len(entity) != 1:
        return cors_response(simplejson.dumps({'error': 'INVALID_PARAMETER', 'error_parameter': 'entity_id', 'success': False}))
    entity = entity[0]

    # Get recipient from entity (this will also confirm the entity and recipient are linked)
    recipient = entity.recipient.filter(pk=recipient_id)
    if len(recipient) != 1:
        return cors_response(simplejson.dumps({'error': 'INVALID_PARAMETER', 'error_parameter': 'recipient_id', 'success': False}))
    recipient = recipient[0]

    payee = recipient.payee
    if payee is None:
        return cors_response(simplejson.dumps({'error': 'NO_PAYEE', 'success': False}))

    print "payee account_id:", payee.account_id