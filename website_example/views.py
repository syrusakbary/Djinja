from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    return render_to_response('index.html',RequestContext(request,{'context_var':'Context variable'}))

def index_haml(request):
    return render_to_response('index.haml',RequestContext(request,{'context_var':'Context variable'}))
