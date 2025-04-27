from rest_framework import serializers
from .models import Tweet, TweetFiles
from django.contrib.auth import get_user_model

User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'profile_image']

    def get_profile_image(self, obj):
        if obj.profile_picture:
            return obj.profile_picture.url
        return '/static/default-avatar.jpg'  # Cambia a tu avatar por defecto



class TweetFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetFiles
        fields = ['file', 'file_type']


class TweetSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    media_files = TweetFilesSerializer(many=True, read_only=True)

    class Meta:
        model = Tweet
        fields = [
            'id',
            'user',
            'content',
            'created_at',
            'likes',
            'retweets',
            'parent_tweet',
            'is_retweet',
            'media_files'
        ]
