from django.shortcuts import render_to_response
from django.template import RequestContext

__author__ = 'Dean Gardiner'


def index(request):
    return render_to_response('home/index.html',
                              context_instance=RequestContext(request, {}))


def login(request):
    return render_to_response('home/login.html',
                              context_instance=RequestContext(request, {}))
