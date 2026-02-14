# File: models.py
# Author: Jake Jeong (jeongsh@bu.edu), 02/13/2026
# Description: Defines database models for the mini_insta app (e.g., Profile).
from django.db import models

# Create your models here.

class Profile(models.Model):
    '''
    Docstring for Profile
    '''

    username = models.TextField(blank=False)
    display_name = models.TextField(blank=False)
    profile_image_url = models.URLField(blank=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now=True)

    def __str__(self):

        return f'{self.username}'



