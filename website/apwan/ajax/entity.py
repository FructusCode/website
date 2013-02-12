import traceback
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from website.apwan.core.api_utils import cors_response, build_error, API_ERROR
from website.apwan.core.deployauth import deployauth_required
from website.apwan.core.entitygen import search_like
from website.apwan.core.entitygen.movie import MovieEntityGenerator
from website.apwan.core.entitygen.music import MusicEntityGenerator
from website.apwan.models.entity import Entity

__author__ = 'Dean Gardiner'


#
# Search
#
@dajaxice_register(method='GET', name='entity.search')
@deployauth_required
def search(request, content_type=None,
           title=None, year=None,
           artist=None, album=None, track=None):
    try:
        if content_type == Entity.TYPE_MUSIC:
            return search_music(title, year, artist, album, track)
        elif content_type == Entity.TYPE_MOVIE:
            return search_movie(title, year, artist, album, track)
        else:
            return cors_response(build_error(API_ERROR.NOT_IMPLEMENTED))
    except Exception:
        print traceback.format_exc()
        return cors_response(build_error(API_ERROR.UNKNOWN))


#
# Music Search
#
def search_music(title, year, artist, album, track):
    if title is not None or year is not None or artist is None:
        return cors_response(build_error(API_ERROR.INVALID_PARAMETER))

    print "TYPE_MUSIC", \
        '"' + str(artist) + '"',\
        '"' + str(album) + '"',\
        '"' + str(track) + '"'

    entities = _direct_search(type=Entity.TYPE_MUSIC,
                              artist=artist, album=album, track=track)
    if entities is None:
        # Lookup Details
        print "looking up"
        entity = MusicEntityGenerator.create(artist, album, track)
        if entity is None:
            return cors_response(build_error(API_ERROR.ENTITY.NOT_FOUND))
        entities = [entity.dict(full=True)]

    return cors_response(simplejson.dumps({
        'success': True,
        'items': entities
    }))


#
# Movie Search
#
def search_movie(title, year, artist, album, track):
    if title is None or year is None:
        return cors_response(build_error(API_ERROR.INVALID_PARAMETER))

    if artist is not None or album is not None or track is not None:
        return cors_response(build_error(API_ERROR.INVALID_PARAMETER))

    print "TYPE_MOVIE", '"' + str(title) + '"'

    entities = _direct_search(type=Entity.TYPE_MOVIE, title=title, year=year)
    if entities is None:
        # Lookup Details
        print "looking up"
        entity = MovieEntityGenerator.create(title, year)
        if entity is None:
            return cors_response(build_error(API_ERROR.ENTITY.NOT_FOUND))
        entities = [entity.dict(full=True)]

    return cors_response(simplejson.dumps({
        'success': True,
        'items': entities
    }))


def _direct_search(type, title=None, year=None,
                   artist=None, album=None, track=None):
    entities = None
    results = None
    if type == Entity.TYPE_MUSIC:
        results = _direct_search_filter(artist=artist, album=album,
                                        track=track)
    elif type == Entity.TYPE_MOVIE:
        results = _direct_search_filter(title=title, year=year)
    else:
        results = _direct_search_filter(title=title)

    if len(results) == 1:
        entities = [results[0].dict(full=True)]
    elif len(results) > 1:
        entities = []
        for entity in results:
            entities.append(entity.dict())

    return entities


def _direct_search_filter(**values):
    query = {}

    if 'title' in values:
        if values['title'] is not None:
            query['s_title__ilike'] = search_like(values['title'])
        else:
            raise ValueError()

        if 'year' in values:
            query['year'] = values['year']
    elif 'artist' in values:
        if values['artist'] is not None:
            query['s_artist__ilike'] = search_like(values['artist'])
        else:
            raise ValueError()  # not None artist required

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
    else:
        raise ValueError()

    print query

    return Entity.objects.all().filter(**query)


def get(request, id):
    pass
