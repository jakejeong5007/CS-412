# File: urls.py
# Author: Jake Jeong (jeongsh@bu.edu), 02/13/2026
# Description: URL routes for the mini_insta app.


from django.urls import path
from . import views
from .views import *

app_name = "voter_analytics"

urlpatterns = [
    path("", views.VoterListView.as_view(), name="voters"),
    path("voter/<int:pk>", views.VoterDetailView.as_view(), name="voter"),
    path("graphs", views.GraphListView.as_view(), name="graphs")
]
