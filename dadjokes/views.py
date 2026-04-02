from django.shortcuts import render
from django.views.generic import *
from .models import *

# Create your views here.

class RandomDetailView(TemplateView):
    """
    TemplateView to show a random picture and joke.
    """
    template_name = "dadjokes/random_dadjoke.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["joke"] = Joke.objects.order_by("?").first()
        context["picture"] = Picture.objects.order_by("?").first()
        return context

class JokesListView(ListView):
    """
    ListView of all jokes.
    """
    model = Joke
    template_name = "dadjokes/show_all_jokes.html"
    context_object_name = "jokes"

class PicturesListView(ListView):
    """
    ListView of all pictures.
    """
    model = Picture
    template_name = "dadjokes/show_all_pictures.html"
    context_object_name = "pictures"

class JokeDetailView(DetailView):
    """
    DetailView for displaying one joke.
    """
    model = Joke
    template_name = "dadjokes/show_joke.html"
    context_object_name = "joke"

class PictureDetailView(DetailView):
    """
    DetailView for displaying one picture.
    """
    model = Picture
    template_name = "dadjokes/show_picture.html"
    context_object_name = "picture"

# Rest API views 
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer

class JokeListAPIView(generics.ListCreateAPIView):
    """
    GET: return all jokes
    POST: create a new joke
    """
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class JokeDetailAPIView(generics.RetrieveAPIView):
    """
    GET: return one joke by primary key
    """
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer


class PictureListAPIView(generics.ListAPIView):
    """
    GET: return all pictures
    """
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class PictureDetailAPIView(generics.RetrieveAPIView):
    """
    GET: return one picture by primary key
    """
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer


class RandomJokeAPIView(APIView):
    """
    GET: return one random joke
    """
    def get(self, request):
        joke = Joke.objects.order_by("?").first()
        serializer = JokeSerializer(joke)
        return Response(serializer.data)


class RandomPictureAPIView(APIView):
    """
    GET: return one random picture
    """
    def get(self, request):
        picture = Picture.objects.order_by("?").first()
        serializer = PictureSerializer(picture)
        return Response(serializer.data)
