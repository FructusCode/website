from dajaxice.decorators import dajaxice_register
import datetime
from django.utils import simplejson
import pytz
from website.apwan.core.api_utils import cors_response, build_error, API_ERROR
from website.apwan.core.deployauth import deployauth_required
from website.apwan.core.entitygen import search_like
from website.apwan.models.recipient import Recipient
from website.apwan.models.token import Token

__author__ = 'Dean Gardiner'


@dajaxice_register(method='GET', name='recipient.search')
@deployauth_required
def search(request, title, limit=10,
           entities_include=False, entities_limit=5,
           lookup_type=None, lookup_token=None):

    results = []
    search_type = None

    if lookup_type is not None and lookup_token is not None:
        # -------------------------------
        #  External "lookup"
        # -------------------------------
        search_type = 'lookup'

        # Find the token in our database
        token = None
        try:
            token = Token.objects.filter(
                token_type=Token.TOKEN_RECIPIENT_LOOKUP,
                token=lookup_token
            )
            if len(token) == 1:
                token = token[0]
            else:
                token = None
        except Token.DoesNotExist:
            pass

        # Check token is still valid
        if token and token.valid():
            token.delete()  # Token has been used, let's remove it.

            if 'title' in token.data and token.data['title'] == title:
                print "TODO: Do the actual lookup"

                # TODO: Do the actual lookup
            else:
                return cors_response(
                    build_error(API_ERROR.RECIPIENT.LOOKUP_TOKEN_INVALID))
        else:
            return cors_response(
                build_error(API_ERROR.RECIPIENT.LOOKUP_TOKEN_INVALID))
    else:
        # -------------------------------
        #   Direct database "search"
        # -------------------------------
        search_type = 'search'

        results = Recipient.objects.all().filter(
            s_title__ilike='%' + search_like(title) + '%'
        )[:limit]

    print "search_type", search_type

    # Append dicts of recipient results
    items = []
    for recipient in results:
        items.append(recipient.dict(
            entities_include=entities_include,
            entities_filter={'parent': None},
            entities_limit=entities_limit,
            check_owner=request.user
        ))

    # Build result dict
    result_dict = {
        'success': True,
        'items': items
    }

    # Create a Token (with a 10 min expire) that can be used for lookups
    if search_type == 'search':
        token = Token.objects.create(
            token_type=Token.TOKEN_RECIPIENT_LOOKUP,

            expire=datetime.datetime.now(
                tz=pytz.utc
            ) + datetime.timedelta(minutes=1),

            data={
                'title': title
            }
        )
        result_dict['lookup_token'] = token.token

    # Return our response
    return cors_response(simplejson.dumps(result_dict))


@dajaxice_register(name='recipient.claim')
@deployauth_required
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
