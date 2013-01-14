import pprint
import musicbrainzngs
from website.apwan.models.entity import Entity
from website.apwan.models.entity_reference import EntityReference
from website.apwan.models.recipient import Recipient
from website.apwan.models.recipient_reference import RecipientReference

__author__ = 'Dean Gardiner'


class MusicEntityGenerator():
    @staticmethod
    def lookup(artist, album=None, track=None):
        query = MusicEntityGenerator._build_query(artist, album, track)
        print query
        results = MusicEntityGenerator._request(query, artist, album, track)

        # Parse result into entity
        if results:
            if track:
                results = results['recording-list']
            elif album:
                results = results['release-list']
            else:
                results = results['artist-list']

            if len(results) > 0:
                _recording = None
                _releases = None
                _artist = None

                if track:
                    _recording, _releases = MusicEntityGenerator._parse_recordings(results)
                    _artist = musicbrainzngs.get_artist_by_id(_recording['artist-credit'][0]['artist']['id'])['artist']
                elif album:
                    _artist, _releases = MusicEntityGenerator._parse_releases(results)
                elif artist:
                    _artist = results[0]

                return _artist, _releases, _recording
        return None

    @staticmethod
    def create(artist, album=None, track=None):
        l_artist, l_releases, l_recording = MusicEntityGenerator.lookup(artist, album, track)

        pprint.pprint(l_releases[0])

        recipient, recipient_ref, created = MusicEntityGenerator.create_artist_recipient(l_artist)

#        if created:
#            print "created"

        e_artist_ref, e_artist, e_artist_created = MusicEntityGenerator.create_entity(l_artist)
        if e_artist_created:
            print "Artist Created"

        if l_releases:
            e_album_ref, e_album, e_album_created = MusicEntityGenerator.create_entity(
                l_artist,
                l_releases[0][0],
                parent=e_artist
            )
            if e_album_created:
                print "Album Created"

        if l_recording:
            e_track_ref, e_track, e_track_created = MusicEntityGenerator.create_entity(
                l_artist,
                l_releases[0][0],
                l_recording,
                parent=e_album
            )
            if e_track_created:
                print "Track Created"
#        else:
#            print "delete all"
#            Entity.objects.all().delete()
#
#            RecipientReference.objects.all().delete()
#            Recipient.objects.all().delete()

        return None

    @staticmethod
    def create_artist_recipient(artist):
        # Search for id in recipient references
        reference_filter = RecipientReference.objects.filter(
            type=RecipientReference.TYPE_MUSICBRAINZ,
            key=artist['id']
        )
        reference_exists = len(reference_filter) == 1
        if reference_exists:
            return reference_filter[0], reference_filter[0].recipient, False

        # Create Recipient
        recipient = Recipient.objects.create(title=artist['name'], type=Recipient.TYPE_M_ARTIST)

        # Create Reference
        reference = RecipientReference.objects.create(
            recipient=recipient,
            type=RecipientReference.TYPE_MUSICBRAINZ,
            key=artist['id']
        )

        return reference, recipient, True

    @staticmethod
    def create_entity(artist, album=None, track=None, parent=None):
        print "create_entity"
        # Search for id in reference
        _key = artist['id']
        if album:
            _key = album['id']
        if track:
            _key = track['id']

        reference_filter = EntityReference.objects.filter(
            type=EntityReference.TYPE_MUSICBRAINZ,
            key=_key
        )
        reference_exists = len(reference_filter) == 1
        if reference_exists:
            print "reference exists", _key
            return reference_filter[0], reference_filter[0].entity, False

        # Create Entity
        _artist = artist['name']
        _album = None
        _track = None
        if album:
            _album = album['title']
        if track:
            _track = track['title']

        entity = Entity.objects.create(
            parent=parent,
            artist=_artist,
            album=_album,
            track=_track,
            type=Entity.TYPE_MUSIC
        )

        # Create Reference
        reference = EntityReference.objects.create(
            entity=entity,
            type=EntityReference.TYPE_MUSICBRAINZ,
            key=_key
        )

        return reference, entity, True


    @staticmethod
    def _build_query(artist, album=None, track=None):
        query = None
        if track and album:
            query = '"' + track + '" artist:"' + artist + '" album:"' + album + '"'
        elif track:
            query = '"' + track + '" artist:"' + artist + '"'
        elif album:
            query = '"' + album + '" artist:"' + artist + '"'
        else:
            query = 'artist:"' + artist + '"'

        return query

    @staticmethod
    def _request(query, artist, album=None, track=None):
        results = None
        if track:
            results = musicbrainzngs.search_recordings(query=query)
        elif album:
            results = musicbrainzngs.search_releases(query=query)
        else:
            results = musicbrainzngs.search_artists(query=query)

        return results

    @staticmethod
    def _get_labels_by_release(release_id):
        labels = musicbrainzngs.browse_labels(release_id)
        if 'label-list' in labels:
            return labels['label-list']
        return None

    @staticmethod
    def _parse_recordings(recordings):
        _recording = None
        _results = []

        for recording in recordings:
            if _recording is None or recording['ext:score'] == _recording['ext:score']:
                _recording = recording

                if 'release-list' in recording:
                    for rel in recording['release-list']:
                        if 'status' in rel and rel['status'] == 'Official':
                            if 'release-group' in rel and 'primary-type' in rel['release-group']:
                                if rel['release-group']['primary-type'] == 'Album':
                                    _labels = MusicEntityGenerator._get_labels_by_release(rel['id'])

                                    if _labels:
                                        _results.append((rel, _labels))
                    recording.pop('release-list')
            else:
                break

        return _recording, _results

    @staticmethod
    def _parse_releases(releases):
        _topRelease = None
        _results = []

        for rel in releases:
            if _topRelease is None or _topRelease['ext:score'] == rel['ext:score']:
                if _topRelease is None:
                    _topRelease = rel

                if 'status' in rel and rel['status'] == 'Official':
                    if 'release-group' in rel and 'primary-type' in rel['release-group']:
                        if rel['release-group']['primary-type'] == 'Album':
                            _labels = MusicEntityGenerator._get_labels_by_release(rel['id'])

                            if _labels:
                                _results.append((rel, _labels))

        _artist = musicbrainzngs.get_artist_by_id(_topRelease['artist-credit'][0]['artist']['id'])['artist']
        return _artist, _results