from rest_framework import serializers
from .models import Hashtag_Results, Hashtag_Search

class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag_Search
        fields = ('ml_model', 'user_hashtag', 'map_bool', 'created_at')

class Results_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag_Results
        fields = ('ml_output', 'bot_heatmap', 'created_at')