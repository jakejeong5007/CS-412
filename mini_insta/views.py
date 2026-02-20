# File: views.py
# Author: Jake Jeong (jeongsh@bu.edu), 02/13/2026
# Description: Class-based views for listing profiles and viewing a single profile.



from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, Post, Photo
from .forms import CreatePostForm

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

class PostDetailView(DetailView):
    """
    DetailView that displays one Post (by pk) using show_post.html.
    """
    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)

        context['profile'] = profile
        return context

    def form_valid(self, form):
        profile_pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=profile_pk)

        post = form.save(commit=False)
        post.profile = profile
        post.save()

        image_url = self.request.POST.get('image_url', '').strip()
        if image_url:
            Photo.objects.create(post=post, image_url=image_url)

        self.object = post
        return super().form_valid(form)
