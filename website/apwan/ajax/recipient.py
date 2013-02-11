from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from website.apwan.ajax.utils import cors_response, build_error, API_ERROR
from website.apwan.core.entitygen import search_like
from website.apwan.models.recipient import Recipient

__author__ = 'Dean Gardiner'


@dajaxice_register(method='GET', name='recipient.search')
def search(request, title, limit=10, entities_include=False, entities_limit=5):
    results = Recipient.objects.all().filter(
        s_title__ilike='%' + search_like(title) + '%'
    )[:limit]

    items = []
    for recipient in results:
        items.append(recipient.dict(
            entities_include=entities_include,
            entities_filter={'parent': None},
            entities_limit=entities_limit,
            check_owner=request.user
        ))

    return cors_response(simplejson.dumps({
        'success': True,
        'items': items
    }))


@dajaxice_register(name='recipient.claim')
def claim(request, recipient_id):
    recipients = Recipient.objects.all().filter(id=recipient_id)
    if len(recipients) == 0:
        return build_error(API_ERROR.INVALID_PARAMETER, recipient_id=recipient_id)
    elif len(recipients) == 1:
        if recipients[0].owner is None:
            if not request.user.is_authenticated():
                return build_error(API_ERROR.AUTHENTICATION.NOT_LOGGED_IN)

            # TODO: Change to manual claim process
            recipients[0].owner = request.user
            recipients[0].save()
            return simplejson.dumps({
                'success': True,
                'recipient': {
                    'id': recipients[0].id,
                    'slug': recipients[0].slug
                }
            })
        else:
            return build_error(API_ERROR.RECIPIENT.ALREADY_CLAIMED)
    else:
        return build_error(API_ERROR.INVALID_PARAMETER, recipient_id=recipient_id)


def get(request, recipient_id):
    pass
