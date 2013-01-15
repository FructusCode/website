import pprint
import traceback
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
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
                return simplejson.dumps({'error': 'INVALID_PARAMETER', 'success': False})

            print "TYPE_MUSIC", '"' + str(artist) + '"', '"' + str(album) + '"', '"' + str(track) + '"'

            results = _entity_search(artist=artist, album=album, track=track)

#            if not album and track:
#                results = Entity.objects.all().filter(artist__iexact=artist, track__iexact=track)
#            else:
#                results = Entity.objects.all().filter(artist__iexact=artist, album__iexact=album, track__iexact=track)

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

            return simplejson.dumps({'success': True, 'items': entities})

        else:
            return simplejson.dumps({'error': 'TYPE_NOT_IMPLEMENTED', 'success': False})

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
        if values['album'] is not None:
            query['s_album__ilike'] = search_like(values['album'])
        else:
            query['album'] = None

    if 'track' in values:
        if values['track'] is not None:
            query['s_track__ilike'] = search_like(values['track'])

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