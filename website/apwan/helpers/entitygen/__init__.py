__author__ = 'Dean Gardiner'

SPECIAL_PHRASES = [
    '~', '`', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=',
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

    for ch in SPECIAL_PHRASES:
        text = text.replace(ch, '')

    return text.strip()


def search_like(text):
    if text is None:
        return None

    for ch in SPECIAL_PHRASES:
        text = text.replace(ch, '%')

    text = text.replace(' ', '%')
    return text.strip('%')