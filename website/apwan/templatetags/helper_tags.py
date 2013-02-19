from django import template
from django.core.urlresolvers import reverse

register = template.Library()

__author__ = 'Dean Gardiner'


@register.simple_tag
def active(request, pattern):
    if not pattern.startswith('/'):
        pattern = reverse(pattern)

    if pattern[-1] != '/' or pattern[-1] != '\\':
        pattern += '/'

    path = request.path
    if path[-1] != '/' or path[-1] != '\\':
        path += '/'

    if request.path.startswith(pattern):
        return 'active'

    return ''


@register.tag
def mustachewrap(parser, token):
    nodelist = parser.parse(('endmustachewrap',))
    parser.delete_first_token()
    return MustacheNode(nodelist)


class MustacheNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context, ):
        output = self.nodelist.render(context)
        return output.replace('[[', '{{').replace(']]', '}}')
