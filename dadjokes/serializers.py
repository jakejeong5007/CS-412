# serializer classes help package the data for transmission over HTTP

from rest_framework import serializers
from .models import *

class JokeSerializer(serializers.ModelSerializer):
    """
    Serializer for joke.
    """
    class Meta:
        model = Joke
        fields = ["name", "text", "timestamp"]

class PictureSerializer(serializers.ModelSerializer):
    """
    Serializer for picture.
    """
    class Meta:
        model = Picture
        fields = ["name", "image_url", "timestamp"]