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
            entities_limit=entities_limit
        ))

    return cors_response(simplejson.dumps({'success': True, 'items': items}))


def get(request, id):
    pass