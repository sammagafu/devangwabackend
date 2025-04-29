from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryListCreateAPIView, CategoryDetailAPIView, UserCategoriesAPIView,
    CommunityJoinAPIView, CommunityLeaveAPIView,
    ThreadListCreateAPIView, ThreadDetailAPIView, UserThreadsAPIView, CommunityThreadsAPIView,
    PostListCreateAPIView, PostDetailAPIView, UserRepliesAPIView,
    IncrementThreadViewsAPIView, LikeThreadAPIView, UnlikeThreadAPIView, ThreadLikesListAPIView,
    LikePostAPIView, UnlikePostAPIView, PostLikesListAPIView,
    ThreadReplyViewSet
)

# Router for ThreadReplyViewSet
router = DefaultRouter()
router.register(r'replies', ThreadReplyViewSet, basename='thread-reply')

urlpatterns = [
    # Category URLs
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<slug:slug>/', CategoryDetailAPIView.as_view(), name='category-detail'),
    path('categories/user/', UserCategoriesAPIView.as_view(), name='user-categories'),
    path('categories/<slug:slug>/join/', CommunityJoinAPIView.as_view(), name='community-join'),
    path('categories/<slug:slug>/leave/', CommunityLeaveAPIView.as_view(), name='community-leave'),

    # Thread URLs
    path('threads/', ThreadListCreateAPIView.as_view(), name='thread-list-create'),
    path('threads/<slug:slug>/', ThreadDetailAPIView.as_view(), name='thread-detail'),
    path('threads/user/', UserThreadsAPIView.as_view(), name='user-threads'),
    path('threads/community/<slug:slug>/', CommunityThreadsAPIView.as_view(), name='community-threads'),
    path('threads/<slug:slug>/increment-views/', IncrementThreadViewsAPIView.as_view(), name='increment-thread-views'),
    path('threads/<slug:slug>/like/', LikeThreadAPIView.as_view(), name='like-thread'),
    path('threads/<slug:slug>/unlike/', UnlikeThreadAPIView.as_view(), name='unlike-thread'),
    path('threads/<slug:slug>/likes/', ThreadLikesListAPIView.as_view(), name='thread-likes-list'),

    # Post (ThreadReply) URLs
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
    path('posts/user/', UserRepliesAPIView.as_view(), name='user-replies'),
    path('posts/<int:pk>/like/', LikePostAPIView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostAPIView.as_view(), name='unlike-post'),
    path('posts/<int:pk>/likes/', PostLikesListAPIView.as_view(), name='post-likes-list'),

    # ThreadReplyViewSet URLs (via router)
    path('', include(router.urls)),
]