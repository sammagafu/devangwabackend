from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryListCreateAPIView, CategoryDetailAPIView,
    ThreadListCreateAPIView, ThreadDetailAPIView,
    PostListCreateAPIView, PostDetailAPIView,
    IncrementThreadViewsAPIView, LikeThreadAPIView,
    UnlikeThreadAPIView, ThreadLikesListAPIView,
    LikePostAPIView, UnlikePostAPIView, PostLikesListAPIView,
    ThreadReplyViewSet
)


router = DefaultRouter()
router.register(r'thread-replies', ThreadReplyViewSet)

urlpatterns = [
    # Category URLs
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    # Thread URLs
    path('threads/', ThreadListCreateAPIView.as_view(), name='thread-list-create'),
    path('threads/<slug:slug>/', ThreadDetailAPIView.as_view(), name='thread-detail'),

    # Post URLs
    path('posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),

    # Thread Views Increment
    path('threads/<slug:slug>/increment_views/', IncrementThreadViewsAPIView.as_view(), name='increment-thread-views'),

    #thread replies
    path('', include(router.urls)),

    # Like and Unlike Thread
    path('threads/<slug:slug>/like/', LikeThreadAPIView.as_view(), name='like-thread'),
    path('threads/<slug:slug>/unlike/', UnlikeThreadAPIView.as_view(), name='unlike-thread'),

    # List Likes for a Thread
    path('threads/<slug:slug>/likes/', ThreadLikesListAPIView.as_view(), name='thread-likes-list'),

    # Like and Unlike Post
    path('posts/<int:pk>/like/', LikePostAPIView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostAPIView.as_view(), name='unlike-post'),

    # List Likes for a Post
    path('posts/<int:pk>/likes/', PostLikesListAPIView.as_view(), name='post-likes-list'),

]
