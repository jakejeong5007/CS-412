# File: urls.py
# Author: Jake Jeong (jeongsh@bu.edu), 02/13/2026
# Description: URL routes for the mini_insta app.


from django.urls import path
from . import views
from .views import *

app_name = "mini_insta"

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),    # /main
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="show_post"),
    path("profile/<int:pk>/create_post", CreatePostView.as_view(), name="create_post"), 
    path("profile/<int:pk>/update", UpdateProfileView.as_view(), name="update_profile"),
    path("post/<int:pk>/delete/", DeletePostView.as_view(), name="delete_post"),
    path("post/<int:pk>/update/", UpdatePostView.as_view(), name="update_post"),
]
