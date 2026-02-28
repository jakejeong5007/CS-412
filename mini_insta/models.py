# File: models.py
# Author: Jake Jeong (jeongsh@bu.edu), 02/13/2026
# Description: Defines database models for the mini_insta app (e.g., Profile).
from django.db import models
from django.urls import reverse

# Create your models here.

class Profile(models.Model):
    '''
    Docstring for Profile
    '''

    username = models.CharField(blank=False)
    display_name = models.CharField(blank=False)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.username}'
    
    def get_all_posts(self):
        '''
        Return a QuerySet of posts from this user
        '''
        posts = Post.objects.filter(profile=self)
        return posts
    
    def get_absolute_url(self):
        return reverse('mini_insta:show_profile', kwargs={'pk': self.pk})


class Post(models.Model): 
    '''
    Docstring for Post
    '''

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
    

class Photo(models.Model):
    '''
    Docstring for Photo
    '''

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
            
