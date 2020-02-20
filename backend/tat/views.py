import requests
from django import http
from django.conf import settings
from django.template import engines
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.exceptions import *

from tat.models import GaussianNB, LSTMTextClassifier

@csrf_exempt
def catchall_dev(request, upstream='http://localhost:3000'):
    """
    Proxy HTTP requests to the frontend dev server in development.

    The implementation is very basic e.g. it doesn't handle HTTP headers.

    """
    upstream_url = upstream + request.path
    method = request.META['REQUEST_METHOD'].lower()
    response = getattr(requests, method)(upstream_url, stream=True)
    content_type = response.headers.get('Content-Type')

    if request.META.get('HTTP_UPGRADE', '').lower() == 'websocket':
        return http.HttpResponse(
            content="WebSocket connections aren't supported",
            status=501,
            reason="Not Implemented"
        )

    elif content_type == 'text/html; charset=UTF-8':
        return http.HttpResponse(
            content=engines['django'].from_string(response.text).render(),
            status=response.status_code,
            reason=response.reason,
        )

    else:
        return http.StreamingHttpResponse(
            streaming_content=response.iter_content(2 ** 12),
            content_type=content_type,
            status=response.status_code,
            reason=response.reason,
        )

catchall_prod = TemplateView.as_view(template_name='index.html')

catchall = catchall_dev if settings.DEBUG else catchall_prod

def search(request):
    if request.method == 'POST':
        user_hashtag = request.POST.get('user_hashtag')
        user_model = request.POST.get('user_model', None)
        #print(user_model)
        if user_model == 'nb':
            print(user_hashtag)
            html = GaussianNB(user_hashtag)
        else:
            html = LSTMTextClassifier('Hashtags', user_hashtag)
        print(user_hashtag)
        return HttpResponse(html)
        #return render(request, 'tat/search.html', user_hashtag)

# Create your views here.
def index(request):
    template = loader.get_template('tat/index.html')
    user_hashtag = ''
    context = {
        'user_hashtag': user_hashtag,

    }
    #return HttpResponse(template.render(context, request))
    return render(request, 'tat/index.html', context)

def about(request):
    template = loader.get_template('tat/about.html')
    context = {

    }
    return render(request, 'tat/about.html', context)
