from django.contrib.auth import get_user_model
from django.db import models
from pixme.apps.base.models import TimestampMixin, UUIDMixin


class Profile(UUIDMixin, TimestampMixin):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=50, blank=True)
    profile_picture = models.ImageField(default='default-user.png', upload_to='profile_images')

    def __str__(self):
        return str(self.user)


class Post(UUIDMixin, TimestampMixin):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='posts')
    content = models.ImageField(upload_to='post_images')
    liked_by = models.ManyToManyField(Profile, through='PostLike', related_name='liked_posts')

    def __str__(self):
        return f"{self.profile.user} - {self.id}"


class PostLike(TimestampMixin):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ['profile', 'post']


class Follow(TimestampMixin):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        unique_together = ['profile', 'follower']


class Comment(TimestampMixin):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=2200)
