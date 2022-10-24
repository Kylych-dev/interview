from rest_framework import serializers 

from ..models import (Post, 
                      LikePost, 
                      FollowersCount, 
                      Profile)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id', 
            'user', 
            'image',
            'caption',
            'created_at',
            'no_of_likes'
        )

class FollowersCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowersCount
        fields = (
            'follower',
            'user',
        )

class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePost
        fields = (
            'post_id',
            'username',
        )

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
                'user',
                'id_user',
                'bio',
                'profile_img',
                'location',

        )