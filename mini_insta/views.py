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

class ShowFollowersDetailView(DetailView):
    """
    DetailView that displays followers of a user using show_followers.html.
    """
    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"


class ShowFollowingDetailView(DetailView):
    """
    DetailView that displays followings of a user using show_following.html.
    """
    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class PostFeedListView(ListView):
    """
    ListView to show the posts of the profiles that the urser is following
    """
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs["pk"])
        context["profile"] = profile
        context["posts"] = profile.get_post_feed()

        return context

class SearchView(ListView):
    """
    SearchView that returns profiles and posts that matches the search query
    """

    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        self.profile = Profile.objects.get(pk=kwargs["pk"])
        if "query" not in request.GET or not request.GET.get("query", "").strip():
            return render(request, "mini_insta/search.html", {"profile": self.profile})

        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        q = self.request.GET.get("query", "").strip()
        return Post.objects.filter(caption__icontains=q).order_by("-timestamp")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        q = self.request.GET.get("query", "").strip()

        context["profile"] = self.profile
        context["query"] = q
        context["posts"] = self.get_queryset()

        by_username = Profile.objects.filter(username__icontains=q)
        by_display = Profile.objects.filter(display_name__icontains=q)
        by_bio = Profile.objects.filter(bio_text__icontains=q)
        context["profiles"] = (by_username | by_display | by_bio).distinct().order_by("username")

        return context
    
