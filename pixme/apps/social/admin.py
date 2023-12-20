from django.contrib import admin
from .models import Profile, Post, PostLike, Follow, Comment

admin.site.register(Post)
admin.site.register(PostLike)
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Comment)
