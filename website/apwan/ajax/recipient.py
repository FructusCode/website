from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from website.apwan.ajax.utils import cors_response
from website.apwan.helpers.entitygen import search_like
from website.apwan.models.recipient import Recipient

__author__ = 'Dean Gardiner'


@dajaxice_register(method='GET', name='recipient.search')
def search(request, title, limit=10, entities_include=False, entities_limit=5):
    results = Recipient.objects.all().filter(s_title__ilike='%' + search_like(title) + '%')[:limit]

    items = []
    for recipient in results:
        items.append(recipient.dict(
            entities_include=entities_include,
            entities_filter={'parent': None},
            entities_limit=entities_limit,
            check_owner=request.user
        ))

    return cors_response(simplejson.dumps({'success': True, 'items': items}))


@dajaxice_register(name='recipient.claim')
def claim(request, recipient_id):
    print "claim", recipient_id

    recipients = Recipient.objects.all().filter(id=recipient_id)
    if len(recipients) == 0:
        return cors_response(simplejson.dumps({'success': False, 'recipient_id': recipient_id}))
    elif len(recipients) == 1:
        if recipients[0].owner is None:
            if not request.user.is_authenticated():
                return cors_response(simplejson.dumps({'success': False, 'recipient_id': recipient_id}))

            recipients[0].owner = request.user
            recipients[0].save()
            return cors_response(simplejson.dumps({'success': True, 'recipient_id': recipient_id}))
        else:
            return cors_response(simplejson.dumps({'success': False, 'recipient_id': recipient_id}))
    else:
        return cors_response(simplejson.dumps({'success': False, 'recipient_id': recipient_id}))


def get(request, recipient_id):
    pass