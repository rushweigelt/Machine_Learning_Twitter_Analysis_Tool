from django.shortcuts import render
import sys
import os
#add path so we can import, as relative import ..tat.ml_models will not work
sys.path.insert(1, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'tat'))
import ml_models




# Create your views here.
def index(request):

    #x = ml_models.RandomForest("foo", True)
    context = {
    }
    if request.GET.get('user_hashtag'):
        # Get our info from the website
        user_hashtag = request.GET.get('user_hashtag')
        user_model = request.GET.get('ml_model', None)
        user_map_bool = request.GET.get('map_bool')
        #decide model and run
        if user_model == 'nb':
            x = ml_models.GaussianNB(user_hashtag, user_map_bool)
            if user_map_bool != None:
                map = "<a href='localhost:8000/heatmap/'>User-Reported Location Heatmap Link </a>"
            else:
                map = ''
            context = {
                "result": x[0],
                'embedded_tweets': x[1],
                "map": map,
            }
            return render(request, 'frontend/index.html', context)
        # Ada Boost
        elif user_model == 'ada':
            x = ml_models.ADA(user_hashtag, user_map_bool)
            if user_map_bool != None:
                map = "<a href='localhost:8000/heatmap/'>User-Reported Location Heatmap Link </a>"
            else:
                map = ''
            context = {
                "result": x[0],
                "embedded_tweets": x[1],
                "map": map
            }
            return render(request, 'frontend/index.html', context)
        # Random Forest
        elif user_model == 'rf':
            x = ml_models.RandomForest(user_hashtag, user_map_bool)
            if user_map_bool != None:
                map = "<a href='localhost:8000/heatmap/'>User-Reported Location Heatmap Link </a>"
            else:
                map = ''
            context = {
                "result": x[0],
                "embedded_tweets": x[1],
                "map": map
            }
            return render(request, 'frontend/index.html', context)
        #LSTM
        elif user_model == 'lstm':
            x = ml_models.LSTMTextClassifier(user_hashtag, user_map_bool)
            if user_map_bool != None:
                map = "<a href='localhost:8000/heatmap/'>User-Reported Location Heatmap Link </a>"
            else:
                map = ''
            context = {
                "result": x[0],
                "embedded_tweets": x[1],
                "map": map
            }
            return render(request, 'frontend/index.html', context)
    #Blank index screen with no results showing
    return render(request, 'frontend/index.html', context)