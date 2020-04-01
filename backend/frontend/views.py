from django.shortcuts import render
import sys
import os
sys.path.insert(1, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tat'))
import ml_models




# Create your views here.
def index(request):

    x = ml_models.RandomForest("foo", True)
    context = {
        "result": x[0],
        "embedded_tweets": x[1],
    }
    return render(request, 'frontend/index.html', context)