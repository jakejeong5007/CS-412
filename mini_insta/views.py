# File: views.py
# Author: Jake Jeong (jeongsh@bu.edu), 02/13/2026
# Description: Class-based views for listing profiles and viewing a single profile.



from django.shortcuts import render
from django.views.generic import *
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm
from django.urls import reverse

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
    """
    CreateView that creates a new post.
    """
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

        # image_url = self.request.POST.get('image_url', '').strip()
        # if image_url:
        #     Photo.objects.create(post=post, image_url=image_url)

        files = self.request.FILES.getlist('files')
        for file in files:
            Photo.objects.create(post=post, image_file=file)

        self.object = post
        return super().form_valid(form)

class UpdateProfileView(UpdateView):
    """
    UpdateView that updates profile information.
    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

class DeletePostView(DeleteView):
    """
    DeleteView that deletes selected post.
    """
    model = Post
    template_name = "mini_insta/delete_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        profile = self.object.profile
        
        context['profile'] = profile 
        context['post'] = post
        return context
    
    def get_success_url(self):
        return reverse("mini_insta:show_profile", kwargs={"pk": self.object.profile.pk})
    

class UpdatePostView(UpdateView):
    """
    UpdateView that updates post caption.
    """
    model = Post
    form_class = UpdatePostForm
    template_name = "mini_insta/update_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        profile = self.object.profile
        
        context['profile'] = profile 
        context['post'] = post
        return context
    
    def get_success_url(self):
        return reverse("mini_insta:show_post", kwargs={"pk": self.object.pk})
