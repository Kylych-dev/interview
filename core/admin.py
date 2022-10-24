from django.contrib import admin
from .models import LikePost, Post, Profile, FollowersCount

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(FollowersCount)


