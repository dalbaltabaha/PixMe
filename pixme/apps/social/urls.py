from django.urls import path
from .views import ProfileView, PostView, FollowView, PostLikeView, CurrentProfileView, CurrentPostView, CommentView, UserSuggestionView

urlpatterns = [
    path('create-profile/', ProfileView.as_view({'post': 'create'}), name='create_profile'),
    path('view-profile/<str:username>/', ProfileView.as_view({'get': 'retrieve'}), name='view_profile'),
    path(
        'current-profile/',
        CurrentProfileView.as_view({
            'delete': 'destroy',
            'get': 'retrieve',
            'put': 'update'
        }),
        name='current_profile'
    ),
    path('create-post/', PostView.as_view({'post': 'create'}), name='create_post'),
    path('view-post/<int:pk>/', PostView.as_view({'get': 'retrieve'}), name='view_post'),
    path('delete-post/<int:pk>/', CurrentPostView.as_view({'delete': 'destroy'}), name='delete_post'),
    path('update-post/<int:pk>/', CurrentPostView.as_view({'put': 'update'}), name='Update_post'),
    path('view-my-posts/', CurrentPostView.as_view({'get': 'list'}), name='view_my_posts'),
    path('follow/', FollowView.as_view({'post': 'create'}), name='follow'),
    path('like-post/', PostLikeView.as_view({'post': 'create'}), name='like'),
    path('comment/', CommentView.as_view({'post': 'create'}), name='comment'),
    path('suggestions/', UserSuggestionView.as_view({'get': 'list'}), name='suggestions')
]
