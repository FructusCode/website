import pprint
import traceback
from dajaxice.decorators import dajaxice_register
from django.http import HttpResponse
from django.utils import simplejson
from website.apwan.ajax.utils import cors_response
from website.apwan.helpers.entitygen import search_like
from website.apwan.helpers.entitygen.music import MusicEntityGenerator
from website.apwan.models.entity import Entity

__author__ = 'Dean Gardiner'


@dajaxice_register(method='GET', name='entity.search')
def search(request, type=None,
           title=None,
           artist=None, album=None, track=None):
    print "entity.search type:", type

    try:
        if type == Entity.TYPE_MUSIC:
            if title is not None or artist is None:
                return cors_response(simplejson.dumps({'error': 'INVALID_PARAMETER', 'success': False}))

            print "TYPE_MUSIC", '"' + str(artist) + '"', '"' + str(album) + '"', '"' + str(track) + '"'

            results = _entity_search(artist=artist, album=album, track=track)

            entities = None

            if len(results) == 1:
                entities = [results[0].dict(full=True)]
            elif len(results) > 1:
                entities = []
                for entity in results:
                    entities.append(entity.dict())
            else:
                # Lookup Details
                print "looking up"

                entity = MusicEntityGenerator.create(artist, album, track)

                entities = [entity.dict(full=True)]

            return cors_response(simplejson.dumps({'success': True, 'items': entities}))

        else:
            return cors_response(simplejson.dumps({'error': 'TYPE_NOT_IMPLEMENTED', 'success': False}))

    except Exception, e:
        print traceback.format_exc()


def _entity_search(**values):
    query = {}

    if 'artist' in values:
        if values['artist'] is not None:
            query['s_artist__ilike'] = search_like(values['artist'])
        else:
            raise ValueError()  # not None artist required
    else:
        raise ValueError()

    if 'album' in values:
        values['album'] = search_like(values['album'])

        if values['album'] is not None and values['album'] != '':
            query['s_album__ilike'] = values['album']
        else:
            query['album'] = None

    if 'track' in values:
        values['track'] = search_like(values['track'])

        if values['track'] is not None and values['track'] != '':
            query['s_track__ilike'] = values['track']

            if 'album' in query and query['album'] is None:
                query.pop('album')
        else:
            query['track'] = None
    else:
        query['track'] = None

    print query

    return Entity.objects.all().filter(**query)


def get(request, id):
    pass