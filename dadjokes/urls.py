from django.urls import path
from . import views
from .views import *

app_name = "dadjokes"


urlpatterns = [
    path("", RandomDetailView.as_view(), name="main"),
    path("random", RandomDetailView.as_view(), name="random"),
    path("jokes", JokesListView.as_view(), name="show_all_jokes"),
    path("joke/<int:pk>", JokeDetailView.as_view(), name="show_joke"),
    path("pictures", PicturesListView.as_view(), name="show_all_pictures"),
    path("picture/<int:pk>", PictureDetailView.as_view(), name="show_picture"),

    # API views
    path("api/", RandomJokeAPIView.as_view(), name='api_main'),
    path("api/random", RandomJokeAPIView.as_view(), name='api_random'),
    path("api/jokes", JokeListAPIView.as_view(), name="api_show_all_jokes"),
    path("api/joke/<int:pk>", JokeDetailAPIView.as_view(), name="api_show_joke"),
    path("api/pictures", JokeListAPIView.as_view(), name="api_show_all_pictures"),
    path("api/picture/<int:pk>", JokeDetailAPIView.as_view(), name="api_show_picture"),
    path("api/random_picture", RandomPictureAPIView.as_view(), name="api_random_picture"),
]