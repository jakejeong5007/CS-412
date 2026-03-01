# File: models.py
# Author: Jake Jeong (jeongsh@bu.edu), 02/13/2026
# Description: Defines database models for the mini_insta app (e.g., Profile).
from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    """
    Profile model
    """

    username = models.CharField(blank=False)
    display_name = models.CharField(blank=False)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.username}'
    
    def get_all_posts(self):
        """
        Return a QuerySet of posts from this user
        """
        posts = Post.objects.filter(profile=self)
        return posts
    
    def get_absolute_url(self):
        return reverse('mini_insta:show_profile', kwargs={'pk': self.pk})
    
    def get_followers(self):
        """
        Returns a list of profiles of people that follows current user
        """
        return [f.follower_profile for f in Follow.objects.filter(profile=self)]
    
    def get_num_followers(self):
        """
        Returns the number of profiles of people that follows current user
        """
        return Follow.objects.filter(profile=self).count()
    
    def get_following(self):
        """
        Returns a list of profiles of people that the user follows
        """
        return [f.profile for f in Follow.objects.filter(follower_profile=self)]

    def get_num_following(self):
        """
        RReturns the number of profiles of people that the user follows
        """
        return Follow.objects.filter(follower_profile=self).count()
    
    def get_post_feed(self):
        """
        Returns queryset of posts from profiles that the user follows
        """
        following_qs = Follow.objects.filter(follower_profile=self).values_list("profile", flat=True)
        return Post.objects.filter(profile__in=following_qs).order_by("-timestamp")


class Post(models.Model): 
    """
    Post model
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.caption}'
    

    def get_all_photos(self):
        '''
        Return a QuerySet of photos associated with this post
        '''
        photos = Photo.objects.filter(post=self)
        return photos
    
    
    def get_absolute_url(self):
        return reverse('mini_insta:show_post', kwargs={'pk': self.pk})
    
    def get_all_comments(self):
        """
        Returns queryset of all comments associated with this post
        """
        return Comment.objects.filter(post=self)

    def get_all_likes(self):
        """
        Returns queryset of al likes associated with this post
        """
        return Like.objects.filter(post=self)
    

class Photo(models.Model):
    """
    Photo model
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)
    image_file = models.ImageField(blank=True)

    def __str__(self):
        if self.image_url:
            return f"Photo(post={self.post}, url={self.image_url})"
        if self.image_file:
            return f"Photo(post={self.post}, url={self.image_file})"
        return f"Photo (no image)"

    def get_image_url(self):
        if self.image_url:
            return self.image_url
        if self.image_file:
            return self.image_file
        return ""
            
class Follow(models.Model):
    """
    Follow model
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.follower_profile.username} follows {self.profile.username}"

class Comment(models.Model):
    """
    Comment model
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField(blank=False)

    def __str__(self):
        return f"Comment by {self.profile.username} on post {self.post}" 

class Like(models.Model):
    """
    Like model
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Like by {self.profile.username} on post {self.post}"

