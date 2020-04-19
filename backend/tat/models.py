'''
Rush Weigelt
Feb 2020
This script is to create serialized json database objects out of every search, thus storing metadata in an organized
and efficient way. This also lessens space needed, as json objects are tiny files
'''

#Django imports
from django.db import models
from .ml_models import GaussianNB, LSTMTextClassifier, RandomForest, ADA
#Choices for our dropdown form, first is how it will be saved, second is how it will be presented
ML_MODEL_CHOICES = (
    ('rf', 'Random Forest'),
    ('nb', 'Naive Bayes'),
    ('ada', 'Ada Boost'),
    ('lstm', 'LSTM'),
)

class Hashtag_Results(models.Model):
    ml_output = models.CharField(max_length=500)
    #bot_heatmap = models.ImageField(upload_to='post_images')
    bot_heatmap = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'tat'
    def __str__(self):
        return self.ml_output
#Models
class Hashtag_Search(models.Model):
    ml_model = models.CharField(max_length=100, choices=ML_MODEL_CHOICES, default='rf')
    user_hashtag = models.CharField(max_length=100, default="foo")
    map_bool = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'tat'
    def __str__(self):
        return self.ml_model+' '+self.user_hashtag

