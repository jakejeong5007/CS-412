# File: serializers.py
# Author: Jake Jeong (jeongsh@bu.edu), 02/13/2026
# Description: Defines serializers for the mini_insta app to convert model data to and from JSON for API use.

from rest_framework import serializers
from .models import Profile, Post, Photo


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "username", "display_name", "profile_image_url", "bio_text", "join_date"]


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "image_url", "timestamp", "image_file"]


class PostSerializer(serializers.ModelSerializer):
    photos = serializers.SerializerMethodField()
    image_url = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Post
        fields = ["id", "profile", "caption", "timestamp", "photos", "image_url"]
        read_only_fields = ["profile", "timestamp", "photos"]

    def get_photos(self, obj):
        photos = Photo.objects.filter(post=obj)
        return PhotoSerializer(photos, many=True).data

    def create(self, validated_data):
        image_url = validated_data.pop("image_url", "")
        post = Post.objects.create(**validated_data)

        if image_url:
            Photo.objects.create(post=post, image_url=image_url)

        return post