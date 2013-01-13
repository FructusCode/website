from dajaxice.decorators import dajaxice_register
from django.utils import simplejson

__author__ = 'Dean Gardiner'


@dajaxice_register(method='POST', name='core.lookup')
def lookup(request):
    return simplejson.dumps({'success': True})