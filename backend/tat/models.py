'''
Rush Weigelt
Feb 2020
This script is to create Django objects out of our ML models
Lots of helper functions
'''

#Django imports
from django.db import models
from .ml_models import GaussianNB, LSTMTextClassifier, RandomForest, ADA

#Models
class Hashtag_Search(models.Model):
    ml_model = None
    user_hashtag = None
    map_bool = False
    created_at = models.DateTimeField(auto_now_add=True)
    results = None

    class Meta:
        app_label = 'tat'
    def __str__(self):
        return self.ml_model+' '+self.user_hashtag

class Hashtag_Results(models.Model):
    search = None
    ml_output = None
    bot_heatmap = None
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'tat'
    def __str__(self):
        return self.ml_output






