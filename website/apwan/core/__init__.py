__author__ = 'Dean Gardiner'


def string_length_limit(text, max_length, limited_suffix="..."):
    text = unicode(text)
    if max_length == -1 or len(text) <= max_length:
        return text
    return text[:max_length - len(limited_suffix)] + limited_suffix
