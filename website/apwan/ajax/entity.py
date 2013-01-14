import pprint
import traceback
from dajaxice.decorators import dajaxice_register
from django.utils import simplejson
from website.apwan import USERAGENT_NAME, USERAGENT_VERSION, USERAGENT_CONTACT
from website.apwan.helpers.metadata.music import MusicMeta
from website.apwan.models.entity import Entity

import musicbrainzngs
musicbrainzngs.set_useragent(USERAGENT_NAME, USERAGENT_VERSION, USERAGENT_CONTACT)

__author__ = 'Dean Gardiner'


@dajaxice_register(method='POST', name='entity.search')
def search(request, type=None,
           title=None,
           artist=None, album=None, track=None):
    print "entity.search type:", type

    if type == Entity.TYPE_MUSIC:
        if title is not None or artist is None:
            return simplejson.dumps({'error': 'INVALID_PARAMETER', 'success': False})

        print "TYPE_MUSIC", '"' + str(artist) + '"', '"' + str(album) + '"', '"' + str(track) + '"'

        results = Entity.objects.all().filter(artist=artist, album=album, track=track)

        if len(results) > 0:
            pass
        else:
            # Lookup Details
            print "looking up"
            try:
                artist, albums, track = MusicMeta.lookup(artist, album, track)

                print 'artist', artist['name']
                if track:
                    print 'track', track['title']

                for release, labels in albums:
                    print release['title'].encode('ascii', 'replace'), "(" + release['country'] + ")"
                    for label in labels:
                        print '\t', label['name'].encode('ascii', 'replace'), "(" + label['country'] + ")"

            except Exception, e:
                print traceback.format_exc()
    else:
        return simplejson.dumps({'error': 'TYPE_NOT_IMPLEMENTED', 'success': False})

    return simplejson.dumps({'success': True})


def get(request, id):
    pass