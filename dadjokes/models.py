from django.db import models

# Create your models here.

class Joke(models.Model):
    name = models.CharField(blank=False)
    text = models.TextField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Joke by {self.name}"


class Picture(models.Model):
    name = models.CharField(blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=False)
    
    def __str__(self):
        return f"Picture by {self.name}"