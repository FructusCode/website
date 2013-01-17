from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

__author__ = 'Dean Gardiner'


@login_required(login_url='/account/login/')
def index(request):
    return render_to_response('account/index.html',
                              context_instance=RequestContext(request, {}))


def payee_add(request):
    return render_to_response('account/payee/add.html',
                              context_instance=RequestContext(request, {}))


def recipient_claim(request):
    return render_to_response('account/recipient/claim.html',
                              context_instance=RequestContext(request, {}))


def report_donations(request):
    return render_to_response('account/report/donations.html',
                              context_instance=RequestContext(request, {}))