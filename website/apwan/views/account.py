from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

__author__ = 'Dean Gardiner'


@login_required(login_url='/account/login/')
def index(request):
    return render_to_response('account/index.html',
                              context_instance=RequestContext(request, {}))