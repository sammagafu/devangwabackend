from rest_framework import serializers
from .models import Category, Thread, ThreadReply, ThreadLike, PostLike
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ThreadLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ThreadLike
        fields = ['id', 'user', 'created_at']

class PostLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'user', 'created_at']

class ThreadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    starter = serializers.ReadOnlyField(source='starter.username')
    likes = ThreadLikeSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['id', 'post', 'category', 'content', 'slug', 'starter', 'created_at', 'views', 'likes', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

class PostSerializer(serializers.ModelSerializer):
    thread = ThreadSerializer(read_only=True)
    author = serializers.ReadOnlyField(source='author.username')
    likes = PostLikeSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = ThreadReply
        fields = ['id', 'thread', 'author', 'content', 'created_at', 'likes', 'likes_count']

    def get_likes_count(self, obj):
        return obj.likes.count()
