# File: urls.py
# Author: Jake Jeong (jeongsh@bu.edu), 02/13/2026
# Description: URL routes for the mini_insta app.


from django.urls import path
from . import views
from .views import *

from django.contrib.auth import views as auth_views

app_name = "mini_insta"

urlpatterns = [
    path("", ProfileListView.as_view(), name="show_all_profiles"),    # /main
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="show_profile"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="show_post"),
    path("post/<int:pk>/delete/", DeletePostView.as_view(), name="delete_post"),
    path("post/<int:pk>/update/", UpdatePostView.as_view(), name="update_post"),
    path("profile/<int:pk>/followers", ShowFollowersDetailView.as_view(), name="show_followers"),
    path("profile/<int:pk>/following", ShowFollowingDetailView.as_view(), name="show_following"),
    path("profile/create_post", CreatePostView.as_view(), name="create_post"), 
    path("profile/update", UpdateProfileView.as_view(), name="update_profile"),
    path("profile/feed", PostFeedListView.as_view(), name="show_feed"),
    path("profile/search", SearchView.as_view(), name="search"),
    path("profile/", MyProfileView.as_view(), name="profile"),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mini_insta:show_all_profiles'), name='logout'),
]
