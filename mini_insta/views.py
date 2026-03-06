# File: views.py
# Author: Jake Jeong (jeongsh@bu.edu), 02/13/2026
# Description: Class-based views for listing profiles and viewing a single profile.



from django.shortcuts import render
from django.views.generic import *
from .models import *
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect

# Create your views here.
class LoginRequiredMixin(LoginRequiredMixin):

    def get_profile(self):
        user = self.request.user
        profile = Profile.objects.get(user=user)
        return profile
    
    def get_object(self):
        return self.get_profile()
    
    def get_login_url(self):
        return reverse('mini_insta:login')

class ProfileListView(ListView):
    """
    Displays all profiles.
    """
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"  
    context_object_name = "profiles"  
    
class CreateProfileView(CreateView):
    """CreateView that will create a profile for a user"""
    model = User
    template_name = 'mini_insta/create_profile_form.html'
    form_class = CreateProfileForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)

        if not user_form.is_valid():
            return self.form_invalid(form)
        
        user = user_form.save()
        login(self.request, user, backend="django.contrib.auth.backends.ModelBackend")
        form.instance.user = user

        return super().form_valid(form)

class ProfileDetailView(DetailView):
    """
    DetailView that displays one Profile (by pk) using show_profile.html.
    """
    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        my_profile = None
        is_following = False

        if self.request.user.is_authenticated:
            my_profile = Profile.objects.get(user=self.request.user)
            is_following = Follow.objects.filter(
                profile=self.object,
                follower_profile=my_profile 
            ).exists()

        context["my_profile"] = my_profile
        context["is_following"] = is_following
        return context

class MyProfileView(LoginRequiredMixin, DetailView):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_profile = None
        has_liked = False

        if self.request.user.is_authenticated:
            my_profile = Profile.objects.get(user=self.request.user)
            has_liked = Like.objects.filter(post=self.object, profile=my_profile).exists()

        context["my_profile"] = my_profile
        context["has_liked"] = has_liked
        return context

class CreatePostView(LoginRequiredMixin, CreateView):
    """
    CreateView that creates a new post.
    """
    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context

    def form_valid(self, form):
        profile = self.get_profile()


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

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """
    UpdateView that updates profile information.
    """
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"

class DeletePostView(LoginRequiredMixin, DeleteView):
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
    

class UpdatePostView(LoginRequiredMixin, UpdateView):
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

class PostFeedListView(LoginRequiredMixin, ListView):
    """
    ListView to show the posts of the profiles that the urser is following
    """
    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = self.get_profile()
        context["profile"] = profile
        context["posts"] = profile.get_post_feed()

        return context

class SearchView(LoginRequiredMixin, ListView):
    """
    SearchView that returns profiles and posts that matches the search query
    """

    template_name = "mini_insta/search_results.html"
    context_object_name = "posts"

    def dispatch(self, request, *args, **kwargs):
        self.profile = self.get_profile()
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

class FollowProfileView(LoginRequiredMixin, TemplateView):
    """
    TemplateView for following an another user
    """
    def dispatch(self, request, *args, **kwargs):
        me = self.get_profile()
        other = Profile.objects.get(pk=kwargs["pk"])

        if me.pk != other.pk:
            if not Follow.objects.filter(profile=other, follower_profile=me).exists():
                Follow.objects.create(profile=other, follower_profile=me)

        return redirect(reverse("mini_insta:show_profile", kwargs={"pk": other.pk}))


class UnfollowProfileView(LoginRequiredMixin, TemplateView):
    """
    TemplateView for unfollowing an another user
    """
    def dispatch(self, request, *args, **kwargs):
        me = self.get_profile()
        other = Profile.objects.get(pk=kwargs["pk"])

        Follow.objects.filter(profile=other, follower_profile=me).delete()

        return redirect(reverse("mini_insta:show_profile", kwargs={"pk": other.pk}))


class LikePostView(LoginRequiredMixin, TemplateView):
    """
    TemplateView for liking an another user's post
    """
    def dispatch(self, request, *args, **kwargs):
        me = self.get_profile()
        post = Post.objects.get(pk=kwargs["pk"])

        if post.profile_id != me.pk:
            if not Like.objects.filter(post=post, profile=me).exists():
                Like.objects.create(post=post, profile=me)

        return redirect(reverse("mini_insta:show_post", kwargs={"pk": post.pk}))


class UnlikePostView(LoginRequiredMixin, TemplateView):
    """
    TemplateView for unliking an another user's post
    """
    def dispatch(self, request, *args, **kwargs):
        me = self.get_profile()
        post = Post.objects.get(pk=kwargs["pk"])

        Like.objects.filter(post=post, profile=me).delete()

        return redirect(reverse("mini_insta:show_post", kwargs={"pk": post.pk}))