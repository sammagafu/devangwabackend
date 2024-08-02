from rest_framework import generics, views, status,permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Category, Thread, ThreadReply, ThreadLike, PostLike
from .serializers import CategorySerializer, ThreadSerializer, ThreadReplySerializer, ThreadLikeSerializer, PostLikeSerializer

# Category Views
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Thread Views
class ThreadListCreateAPIView(generics.ListCreateAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(starter=self.request.user)
 
class ThreadDetailAPIView(generics.RetrieveAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    lookup_field = 'slug'

# Post Views
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = ThreadReply.objects.all()
    serializer_class = ThreadReplySerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = ThreadReply.objects.all()
    serializer_class = ThreadReplySerializer

# Increment Thread Views
class IncrementThreadViewsAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, slug):
        thread = get_object_or_404(Thread, slug=slug)
        thread.views += 1
        thread.save()
        return Response({'status': 'views incremented', 'views': thread.views})

# Like Thread
class LikeThreadAPIView(views.APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        thread = get_object_or_404(Thread, slug=self.kwargs['slug'])
        return ThreadLike.objects.filter(thread=thread)

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
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post = get_object_or_404(ThreadReply, pk=self.kwargs['pk'])
        return PostLike.objects.filter(post=post)
        pagination_class = None  # Add this if you don't want pagination for listing likes
