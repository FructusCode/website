from django import template

register = template.Library()

__author__ = 'Dean Gardiner'


@register.filter
def truncate(string, max_length):
    """ Truncate the {string} to {max_length} characters

    usage  : {{ "text longer than 6 chars"|truncate:9 }}
    result : "text long"
    """
    string = str(string)

    if len(string) > max_length:
        return string[:max_length]
    return string
