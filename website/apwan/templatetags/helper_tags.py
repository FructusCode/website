from django import template
from django.core.urlresolvers import reverse

register = template.Library()

__author__ = 'Dean Gardiner'


@register.simple_tag
def active(request, pattern):
    if not pattern.startswith('/'):
        pattern = reverse(pattern)

    if request.path.startswith(pattern):
        return 'active'

    return ''
