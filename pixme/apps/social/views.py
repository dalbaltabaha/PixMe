from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from pixme.apps.rest.serializers import (
    ProfileSerializer,
    PostSerializer,
    FollowSerializer,
    PostLikeSerializer,
    CommentSerializer
)
from rest_framework.permissions import IsAuthenticated
from .models import Post, Profile


class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    def get_queryset(self):
        return get_user_model().objects.all()

    def get_object(self):
        instance = super().get_object()
        return (
            Profile.
            objects.
            annotate(
                follower_count=Count('followers'),
                following_count=Count('following'),
                post_count=Count('posts')
            )
            .get(user=instance)
        )


class CurrentProfileView(mixins.UpdateModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.DestroyModelMixin,
                         GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return (
            Profile.
            objects.
            annotate(
                follower_count=Count('followers'),
                following_count=Count('following'),
                post_count=Count('posts')
            )
            .get(user=self.request.user)
        )


class PostView(mixins.CreateModelMixin,
               mixins.RetrieveModelMixin,
               GenericViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.annotate(like_count=Count('liked_by'))

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


class CurrentPostView(mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.profile.posts.all()


class FollowView(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    # return Profile.objects.exclude(user=self.request.user)


class PostLikeView(viewsets.ModelViewSet):
    serializer_class = PostLikeSerializer
    permission_classes = [IsAuthenticated]


class CommentView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Post.objects.all()


class UserSuggestionView(mixins.ListModelMixin, GenericViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.exclude(followers__follower__user=self.request.user).exclude(user=self.request.user)
