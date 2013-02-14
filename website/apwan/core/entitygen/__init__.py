import unicodedata
from website.apwan.models.entity import Entity
from website.apwan.models.entity_reference import EntityReference
from website.apwan.models.recipient import Recipient
from website.apwan.models.recipient_reference import RecipientReference

SPECIAL_PHRASES = [
    '~', '`', '!', '@', '#', '$', '%', '^',
    '&', '*', '(', ')', '_', '-', '+', '=',
    ',', '.', '/', '?',
    ':', ';', '"', "'",
    '[', ']', '{', '}',
    '\\', '|',

    u"\u2019",

    'and'
]


def search_strip(text):
    if text is None:
        return None

    if type(text) is unicode:
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

    for ch in SPECIAL_PHRASES:
        text = text.replace(ch, '')

    return text.strip()


def search_like(text):
    if text is None:
        return None

    if type(text) is unicode:
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore')

    for ch in SPECIAL_PHRASES:
        text = text.replace(ch, '%')

    text = text.replace(' ', '%')
    return text.strip('%')


class EntityGenerator():
    def __init__(self):
        pass

    @staticmethod
    def create_recipient(key, title, ref_type, type):
        # Search for id in recipient references
        reference_filter = RecipientReference.objects.filter(
            type=ref_type,
            key=key
        )
        reference_exists = len(reference_filter) == 1
        if reference_exists:
            return reference_filter[0], reference_filter[0].recipient, False

        # Create Recipient
        recipient = Recipient.objects.create(
            title=title,
            s_title=search_strip(title),
            type=type
        )

        # Create Reference
        reference = RecipientReference.objects.create(
            recipient=recipient,
            type=ref_type,
            key=key
        )

        return reference, recipient, True

    @staticmethod
    def create_entity(id, ref_type, type, title=None, year=None,
                      artist=None, album=None, track=None, parent=None):

        reference_filter = EntityReference.objects.filter(
            type=ref_type,
            key=id
        )
        reference_exists = len(reference_filter) == 1
        if reference_exists:
            print "reference exists", id
            return reference_filter[0], reference_filter[0].entity, False

        # Create Entity
        entity = Entity.objects.create(
            parent=parent,
            # Music
            artist=artist,
            album=album,
            track=track,
            # TV Show, Movie, Game
            title=title,
            # Movie
            year=year,
            # Search Fields
            s_title=search_strip(title),
            s_artist=search_strip(artist),
            s_album=search_strip(album),
            s_track=search_strip(track),
            type=type
        )

        # Create Reference
        reference = EntityReference.objects.create(
            entity=entity,
            type=ref_type,
            key=id
        )

        return reference, entity, True
