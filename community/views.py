from rest_framework import generics, views, status, permissions, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .models import Category, Thread, ThreadReply, ThreadLike, PostLike, CommunityFollowers
from .serializers import CategorySerializer, ThreadSerializer, ThreadReplySerializer, ThreadLikeSerializer, PostLikeSerializer

# Pagination
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Category Views
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all().prefetch_related('followers__user', 'threads__starter', 'threads__replies__author', 'threads__likes__user')
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'slug']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all().prefetch_related('followers__user', 'threads__starter', 'threads__replies__author', 'threads__likes__user')
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserCategoriesAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Category.objects.filter(followers__user=self.request.user).prefetch_related('followers__user', 'threads__starter')

class CommunityJoinAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        follow, created = CommunityFollowers.objects.get_or_create(user=request.user, community=category)
        if not created:
            return Response({'status': 'already following'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'followed', 'follower_count': category.followers.count()})

class CommunityLeaveAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        try:
            follow = CommunityFollowers.objects.get(user=request.user, community=category)
            follow.delete()
            return Response({'status': 'not following'}, status=status.HTTP_400_BAD_REQUEST)
        except CommunityFollowers.DoesNotExist:
            return Response({'status': 'not following'}, status=status.HTTP_400_BAD_REQUEST)

# Thread Views
class ThreadListCreateAPIView(generics.ListCreateAPIView):
    queryset = Thread.objects.all().select_related('starter', 'category').prefetch_related(
        'replies__author', 'replies__likes__user', 'replies__child_replies__author', 'replies__child_replies__likes__user', 'likes__user'
    )
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'starter', 'is_community_post']
    search_fields = ['content']
    ordering_fields = ['created_at', 'views', 'likes_count']

    def perform_create(self, serializer):
        serializer.save(starter=self.request.user)

class ThreadDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Thread.objects.all().select_related('starter', 'category').prefetch_related(
        'replies__author', 'replies__likes__user', 'replies__child_replies__author', 'replies__child_replies__likes__user', 'likes__user'
    )
    serializer_class = ThreadSerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserThreadsAPIView(generics.ListAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Thread.objects.filter(starter=self.request.user).select_related('starter', 'category').prefetch_related(
            'replies__author', 'replies__likes__user', 'replies__child_replies__author', 'replies__child_replies__likes__user', 'likes__user'
        )

class CommunityThreadsAPIView(generics.ListAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Thread.objects.filter(category=category).select_related('starter', 'category').prefetch_related(
            'replies__author', 'replies__likes__user', 'replies__child_replies__author', 'replies__child_replies__likes__user', 'likes__user'
        )

# Post (ThreadReply) Views
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = ThreadReply.objects.all().select_related('author', 'thread', 'parent').prefetch_related(
        'likes__user', 'child_replies__author', 'child_replies__likes__user'
    )
    serializer_class = ThreadReplySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['thread', 'author']
    search_fields = ['content']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ThreadReply.objects.all().select_related('author', 'thread', 'parent').prefetch_related(
        'likes__user', 'child_replies__author', 'child_replies__likes__user'
    )
    serializer_class = ThreadReplySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class UserRepliesAPIView(generics.ListAPIView):
    serializer_class = ThreadReplySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return ThreadReply.objects.filter(author=self.request.user).select_related('author', 'thread', 'parent').prefetch_related(
            'likes__user', 'child_replies__author', 'child_replies__likes__user'
        )

# Increment Thread Views
class IncrementThreadViewsAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, slug):
        thread = get_object_or_404(Thread, slug=slug)
        thread.increase_views()
        return Response({'status': 'views incremented', 'views': thread.views})

# Like Thread
class LikeThreadAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        thread = get_object_or_404(Thread, slug=slug)
        like, created = ThreadLike.objects.get_or_create(user=request.user, thread=thread)
        if not created:
            return Response({'status': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'liked', 'likes_count': thread.likes.count()})

# Unlike Thread
class UnlikeThreadAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        thread = get_object_or_404(Thread, slug=slug)
        try:
            like = ThreadLike.objects.get(user=request.user, thread=thread)
            like.delete()
            return Response({'status': 'unliked', 'likes_count': thread.likes.count()})
        except ThreadLike.DoesNotExist:
            return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)

# List Likes for a Thread
class ThreadLikesListAPIView(generics.ListAPIView):
    serializer_class = ThreadLikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        thread = get_object_or_404(Thread, slug=self.kwargs['slug'])
        return ThreadLike.objects.filter(thread=thread).select_related('user')

# Like Post
class LikePostAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(ThreadReply, pk=pk)
        like, created = PostLike.objects.get_or_create(user=request.user, post=post)
        if not created:
            return Response({'status': 'already liked'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'liked', 'likes_count': post.likes.count()})

# Unlike Post
class UnlikePostAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(ThreadReply, pk=pk)
        try:
            like = PostLike.objects.get(user=request.user, post=post)
            like.delete()
            return Response({'status': 'unliked', 'likes_count': post.likes.count()})
        except PostLike.DoesNotExist:
            return Response({'status': 'not liked'}, status=status.HTTP_400_BAD_REQUEST)

# List Likes for a Post
class PostLikesListAPIView(generics.ListAPIView):
    serializer_class = PostLikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        post = get_object_or_404(ThreadReply, pk=self.kwargs['pk'])
        return PostLike.objects.filter(post=post).select_related('user')

# Thread Reply ViewSet
class ThreadReplyViewSet(viewsets.ModelViewSet):
    queryset = ThreadReply.objects.all().select_related('author', 'thread', 'parent').prefetch_related(
        'likes__user', 'child_replies__author', 'child_replies__likes__user'
    )
    serializer_class = ThreadReplySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['thread', 'author', 'created_at']
    search_fields = ['content']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)