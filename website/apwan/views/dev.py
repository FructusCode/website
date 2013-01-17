from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

__author__ = 'Dean Gardiner'


@login_required(login_url='/account/login/')
def index(request):
    return render_to_response('dev/index.html',
                              context_instance=RequestContext(request, {}))


@login_required(login_url='/account/login/')
def search(request):
    return render_to_response('dev/search.html',
                              context_instance=RequestContext(request, {}))