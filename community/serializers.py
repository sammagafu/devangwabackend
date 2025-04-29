from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Thread, ThreadReply, ThreadLike, PostLike, CommunityFollowers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email']

class CommunityFollowersSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CommunityFollowers
        fields = ['user', 'created_at']

class CategorySerializer(serializers.ModelSerializer):
    followers = CommunityFollowersSerializer(many=True, read_only=True)
    threads = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'followers', 'threads', 'follower_count']

    def get_threads(self, obj):
        threads = obj.threads.all()
        return ThreadSerializer(threads, many=True, context=self.context).data

    def get_follower_count(self, obj):
        return obj.followers.count()

class PostLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ['user', 'post', 'created_at']

class ThreadLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ThreadLike
        fields = ['user', 'thread', 'created_at']

class ThreadReplySerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes = PostLikeSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = ThreadReply
        fields = ['id', 'thread', 'author', 'content', 'created_at', 'parent', 'likes', 'likes_count', 'replies', 'replies_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_replies(self, obj):
        replies = obj.child_replies.all()
        return ThreadReplySerializer(replies, many=True, context=self.context).data

    def get_replies_count(self, obj):
        return obj.child_replies.count()

class ThreadSerializer(serializers.ModelSerializer):
    starter = UserSerializer(read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    replies = ThreadReplySerializer(many=True, read_only=True)
    likes = ThreadLikeSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Thread
        fields = ['id', 'post', 'category', 'content', 'slug', 'starter', 'created_at', 'views', 'is_community_post', 'replies', 'likes', 'likes_count', 'replies_count']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_replies_count(self, obj):
        return obj.replies.count()