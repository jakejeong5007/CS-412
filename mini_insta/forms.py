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
    

class DeletePostForm(forms.ModelForm):
    """A form to delete a post"""

    class Meta:
        model = Post
        fields = ['profile']

class UpdatePostForm(forms.ModelForm):
    """A form to update post information"""

    class Meta:
        model = Post
        fields = ['caption']


class CreateProfileForm(forms.ModelForm):
    """A form to create a user profile"""

    class Meta:
        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']
