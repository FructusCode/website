from django import template

register = template.Library()

__author__ = 'Dean Gardiner'

@register.simple_tag
def active(request, pattern):
    if request.path.startswith(pattern):
        return 'active'
    return ''