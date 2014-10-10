from django.shortcuts import render
from django.shortcuts import render,render_to_response,RequestContext
from django.http import HttpResponse,HttpResponseRedirect,Http404

import feed.helper
from feed.tasks import *
# Create your views here.


def test(request):
    return HttpResponse()

