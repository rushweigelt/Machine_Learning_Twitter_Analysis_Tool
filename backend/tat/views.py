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

from .models import GaussianNB, LSTMTextClassifier, RandomForest, ADA, Hashtag_Results, Hashtag_Search

from .serializers import Search_Serializer, Results_Serializer
from rest_framework import generics

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
            #print(user_model)
            html = GaussianNB(user_hashtag)
        elif user_model == 'RandomForest':
            #print(user_model)
            html = RandomForest(user_hashtag)
        elif user_model == 'ada':
            #print(user_model)
            html = ADA(user_hashtag)
        elif user_model == 'lstm':
            #print(user_model)
            html = LSTMTextClassifier(user_hashtag)
        print(user_hashtag)
        return HttpResponse(html)
        #return render(request, 'tat/search.html', user_hashtag)

# Create your views here.
def index(request):
    context ={

    }
    if request.GET.get('user_hashtag'):
        #Get our info from the website
        user_hashtag = request.GET.get('user_hashtag')
        user_model = request.GET.get('user_model', None)
        user_map_bool = request.GET.get('user_map_bool')
        #Assign vars to our new search Model Object
        search = Hashtag_Search()
        search.user_hashtag = user_hashtag
        search.ml_model = user_model
        search.map_bool = user_map_bool
        #Assign vars to our new Results Model Object
        #results = Hashtag_Results()
        #x = RandomForest(user_hashtag, user_map_bool)
        #results.ml_output = x[0]
        #results.bot_heatmap = "<a href='localhost:8000/heatmap/'>User-Reported Location Heatmap Link </a>"
        #User Picks a Model
        #Naive Bayes
        if user_model == 'nb':
            x = GaussianNB(user_hashtag, user_map_bool)
            if user_map_bool != None:
                map = "<a href='localhost:8000/heatmap/'>User-Reported Location Heatmap Link </a>"
            else:
                map = ''
            #Create our Database Items
            response = Hashtag_Results()
            response.ml_output = x[0]
            response.bot_heatmap = None
            response.search = search
            search.results = response

            context = {
                "result" : x[0],
                'embedded_tweets': x[1],
                "map": map,
            }
            return render(request, 'tat/index.html', context)
        #Ada Boost
        elif user_model == 'ada':
            x = ADA(user_hashtag, user_map_bool)
            if user_map_bool != None:
                map = "<a href='localhost:8000/heatmap/'>User-Reported Location Heatmap Link </a>"
            else:
                map = ''
            #Create our Database Items
            response = Hashtag_Results()
            response.ml_output = x[0]
            response.bot_heatmap = None
            response.search = search
            search.results = response

            context = {
                "result": x[0],
                "embedded_tweets": x[1],
                "map": map
            }
            return render(request, 'tat/index.html', context)
        #Random Forest
        elif user_model == 'rf':
            x = RandomForest(user_hashtag, user_map_bool)
            if user_map_bool == True:
                map = "<a href='localhost:8000/heatmap/'>User-Reported Location Heatmap Link </a>"
            else:
                map = ''
            response = Hashtag_Results()
            response.ml_output = x[0]
            response.bot_heatmap = map
            context = {
                "result": x[0],
                "embedded_tweets": x[1],
                "map": map
            }
            return render(request, 'tat/index.html', context)
        elif user_model == 'lstm':
            x = LSTMTextClassifier(user_hashtag, user_map_bool)
            if user_map_bool != None:
                map = "<a href='localhost:8000/heatmap/'>User-Reported Location Heatmap Link </a>"
            else:
                map = ''
            #Create our Database Items
            response = Hashtag_Results()
            response.ml_output = x[0]
            response.bot_heatmap = None
            response.search = search
            search.results = response
            # print(x[1])
            context = {
                "result": x[0],
                "embedded_tweets": x[1],
                "map": map
            }
    return render(request, 'tat/index.html', context)

'''
def index(request):
    template = loader.get_template('tat/index.html')
    user_hashtag = ''
    context = {
        'user_hashtag': user_hashtag,

    }
    #return HttpResponse(template.render(context, request))
    return render(request, 'tat/index.html', context)
'''
def about(request):
    #template = loader.get_template('tat/about.html')
    context = {

    }
    return render(request, 'tat/about.html', context)

def purpose(request):
    #template = loader.get_template('tat/about.html')
    context = {

    }
    return render(request, 'tat/purpose.html', context)

def heatmap(request):
    context = {

    }
    return render(request, 'tat/heatmap.html', context)

class HashtagSearchCreate(generics.ListCreateAPIView):
    queryset = Hashtag_Search.objects.all()
    serializer_class = Search_Serializer

class HashtagResultsCreate(generics.ListCreateAPIView):
    queryset = Hashtag_Results.objects.all()
    serializer_class = Results_Serializer
