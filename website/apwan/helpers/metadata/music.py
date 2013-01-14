import musicbrainzngs

__author__ = 'Dean Gardiner'


class MusicMeta():
    @staticmethod
    def lookup(artist, album=None, track=None):
        query = MusicMeta._build_query(artist, album, track)
        results = MusicMeta._request(query, artist, album, track)

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
                _releases = []
                _artist = None

                if track:
                    _recording, _releases = MusicMeta._parse_recordings(results)
                    _artist = musicbrainzngs.get_artist_by_id(_recording['artist-credit'][0]['artist']['id'])['artist']
                elif album:
                    _artist, _releases = MusicMeta._parse_releases(results)
                elif artist:
                    _artist = results[0]

                return _artist, _releases, _recording
        return None

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
                        if rel['status'] == 'Official':
                            _labels = MusicMeta._get_labels_by_release(rel['id'])

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

                if rel['status'] == 'Official':
                    _labels = MusicMeta._get_labels_by_release(rel['id'])

                    if _labels:
                        _results.append((rel, _labels))

        _artist = musicbrainzngs.get_artist_by_id(_topRelease['artist-credit'][0]['artist']['id'])['artist']
        return _artist, _results