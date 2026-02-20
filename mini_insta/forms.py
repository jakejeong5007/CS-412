from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """A from to add an Post to the database"""

    class Meta:
        """ associate this form with a model from our databse"""
        model = Post
        fields = ['caption']