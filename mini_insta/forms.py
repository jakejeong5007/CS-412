from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """A form to add a Post to the database"""

    class Meta:
        """ associate this form with a model from our databse"""
        model = Post
        fields = ['caption']


class UpdateProfileForm(forms.ModelForm):
    """A form to update profile information """

    class Meta:
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']
    
    