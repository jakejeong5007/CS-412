# File: views.py
# Author: Jake Jeong (jeongsh@bu.edu), 02/13/2026
# Description: Class-based views for listing profiles and viewing a single profile.



from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile

# Create your views here.
class ProfileListView(ListView):
    """
    Displays all profiles.
    """
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"  
    context_object_name = "profiles"  
    
class ProfileDetailView(DetailView):
    """
    DetailView that displays one Profile (by pk) using show_profile.html.
    """
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"