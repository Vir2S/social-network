from rest_framework import serializers
from .models import Post, Like, Dislike, SocialUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        fields = (
            'username', 'password', 'first_name'
        )


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialUser
        fields = (
            'last_login',
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id', 'post_text', 'post_published', 'post_user'
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = (
            'like_user', 'like_post', 'like', 'liked_at'
        )


class DislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dislike
        fields = (
            'dislike_user', 'dislike_post', 'dislike', 'disliked_at'
        )
