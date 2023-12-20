from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

from pixme.apps.base.rest.serializers import CurrentProfileDefault
from pixme.apps.social.models import Profile, Post, Follow, PostLike, Comment


class FollowableProfileField(serializers.SlugRelatedField):
    def get_queryset(self):
        request = self.parent.context.get('request')
        return Profile.objects.exclude(user=request.user)


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=CurrentUserDefault())
    follower_count = serializers.IntegerField(read_only=True)
    following_count = serializers.IntegerField(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        fields = (
            'uuid', 'user', 'bio', 'location', 'profile_picture', 'follower_count', 'following_count', 'post_count',
            'username'
        )


class SimpleCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='profile.user.username', read_only=True)

    # profile = ProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'username', 'comment')


class PostSerializer(serializers.ModelSerializer):
    content = serializers.ImageField(use_url=True)
    like_count = serializers.IntegerField(read_only=True)
    comments = SimpleCommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = ('uuid', 'content', 'liked_by', 'created_at', 'like_count', 'comments')


class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.HiddenField(default=CurrentProfileDefault())
    profile = FollowableProfileField(slug_field='uuid')

    class Meta:
        model = Follow
        fields = ('follower', 'profile')


class PostLikeSerializer(serializers.ModelSerializer):
    profile = serializers.HiddenField(default=CurrentProfileDefault())
    post = serializers.SlugRelatedField(slug_field='uuid', queryset=Post.objects.all())

    class Meta:
        model = PostLike
        fields = ('profile', 'post')


class CommentSerializer(serializers.ModelSerializer):
    profile = serializers.HiddenField(default=CurrentProfileDefault())
    post = serializers.SlugRelatedField(slug_field='uuid', queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = ('id', 'profile', 'post', 'comment')
