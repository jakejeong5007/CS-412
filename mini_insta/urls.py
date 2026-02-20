# File: urls.py
# Author: Jake Jeong (jeongsh@bu.edu), 02/13/2026
# Description: URL routes for the mini_insta app.


from django.urls import path
from . import views
from .views import ProfileListView, ProfileDetailView, PostDetailView, CreatePostView

app_name = "mini_insta"

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),    # /main
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="show_post"),
    path("profile/<int:pk>/create_post", CreatePostView.as_view(), name="create_post"), 
]
