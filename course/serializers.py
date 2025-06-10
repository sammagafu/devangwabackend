# course/serializers.py
from rest_framework import serializers
from .models import Course, Module, Video, Document, Quiz, Question, Answer, Enrollment, VideoProgress, DocumentProgress, QuizAttempt, ModuleProgress, FAQ, Tags,CourseReview
from django.contrib.auth import get_user_model
from django.utils.text import slugify
User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']

# Tags Serializer
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'tag', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

# FAQ Serializer
class FAQSerializer(serializers.ModelSerializer):
    is_asked_by = UserSerializer(read_only=True)
    is_answered_by = UserSerializer(read_only=True)

    class Meta:
        model = FAQ
        fields = [
            'id', 'course', 'question', 'answer', 'created_at', 'replied_at',
            'is_answered', 'is_visible', 'is_edited_at', 'is_asked_by', 'is_answered_by'
        ]
        read_only_fields = ['id', 'created_at', 'replied_at', 'is_edited_at', 'is_asked_by', 'is_answered_by']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['is_asked_by'] = request.user if request else None
        if validated_data.get('is_answered'):
            validated_data['is_answered_by'] = request.user if request else None
        return super().create(validated_data)

# Answer Serializer
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']
        read_only_fields = ['id']

# Question Serializer
class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'explanation', 'answers']
        read_only_fields = ['id']

# Quiz Serializer
class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'slug', 'description', 'pass_mark', 'total_marks', 'time_limit', 'questions']
        read_only_fields = ['id', 'slug']

# Video Serializer
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'slug', 'video_url']
        read_only_fields = ['id', 'slug']

# Document Serializer
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'slug', 'document_file']
        read_only_fields = ['id', 'slug']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order']  # Exclude slug

    def validate(self, data):
        title = data.get('title')
        course_id = self.context['course_id']
        instance = self.instance

        if title:
            slug = slugify(title)
            # Check for slug uniqueness within the course
            queryset = Module.objects.filter(course_id=course_id, slug=slug)
            if instance:
                queryset = queryset.exclude(id=instance.id)

            if queryset.exists():
                # Append counter to ensure unique slug
                counter = 1
                while Module.objects.filter(course_id=course_id, slug=f"{slug}-{counter}").exists():
                    counter += 1
                data['slug'] = f"{slug}-{counter}"
            else:
                data['slug'] = slug

        return data

    def create(self, validated_data):
        validated_data['course_id'] = self.context['course_id']
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
# Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    faqs = FAQSerializer(many=True, required=False)
    tags = TagsSerializer(many=True, required=False)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'instructor', 'price', 'ispublished', 'cover',
            'created_at', 'updated_at', 'discount_percentage', 'discount_deadline', 'total_modules',
            'total_videos', 'total_documents', 'total_quizzes', 'tags', 'is_featured', 'modules',
            'faqs', 'final_price'
        ]
        read_only_fields = [
            'id', 'slug', 'instructor', 'created_at', 'updated_at', 'final_price',
            'total_modules', 'total_videos', 'total_documents', 'total_quizzes', 'modules','reviews'
        ]

    def create(self, validated_data):
        faqs_data = validated_data.pop('faqs', [])
        tags_data = validated_data.pop('tags', [])
        course = Course.objects.create(**validated_data)
        for faq_data in faqs_data:
            FAQ.objects.create(course=course, **faq_data)
        for tag_data in tags_data:
            tag, created = Tags.objects.get_or_create(tag=tag_data['tag'])
            course.tags.add(tag)
        return course

    def update(self, instance, validated_data):
        # Handle related fields
        faqs_data = validated_data.pop('faqs', [])
        tags_data = validated_data.pop('tags', [])

        # Update scalar fields
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.ispublished = validated_data.get('ispublished', instance.ispublished)
        instance.discount_percentage = validated_data.get('discount_percentage', instance.discount_percentage)
        instance.discount_deadline = validated_data.get('discount_deadline', instance.discount_deadline)
        instance.is_featured = validated_data.get('is_featured', instance.is_featured)
        if 'cover' in validated_data:
            instance.cover = validated_data['cover']
        instance.save()

        # Update FAQs
        instance.faqs.all().delete()  # Clear existing FAQs
        for faq_data in faqs_data:
            FAQ.objects.create(course=instance, **faq_data)

        # Update Tags
        instance.tags.clear()  # Clear existing tags
        for tag_data in tags_data:
            tag, created = Tags.objects.get_or_create(tag=tag_data['tag'])
            instance.tags.add(tag)

        return instance

# Enrollment Serializer
class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    last_accessed_module = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            'id', 'user', 'course', 'enrolled_at', 'completion_percentage', 'is_completed',
            'started_at', 'completed_at', 'last_accessed_module', 'progress_notes', 'certificate_issued'
        ]
        read_only_fields = [
            'id', 'user', 'course', 'enrolled_at', 'completion_percentage', 'is_completed',
            'started_at', 'completed_at', 'certificate_issued'
        ]

    def get_last_accessed_module(self, obj):
        if obj.last_accessed_module:
            return {'id': obj.last_accessed_module.id, 'title': obj.last_accessed_module.title}
        return None

# VideoProgress Serializer
class VideoProgressSerializer(serializers.ModelSerializer):
    video = serializers.PrimaryKeyRelatedField(queryset=Video.objects.all())

    class Meta:
        model = VideoProgress
        fields = ['id', 'video', 'watched', 'watched_at', 'last_position']
        read_only_fields = ['id', 'watched_at']

# DocumentProgress Serializer
class DocumentProgressSerializer(serializers.ModelSerializer):
    document = serializers.PrimaryKeyRelatedField(queryset=Document.objects.all())

    class Meta:
        model = DocumentProgress
        fields = ['id', 'document', 'read', 'read_at', 'page_number']
        read_only_fields = ['id', 'read_at']

# QuizAttempt Serializer
class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz = serializers.PrimaryKeyRelatedField(queryset=Quiz.objects.all())

    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'score', 'passed', 'attempted_at', 'user_answers']
        read_only_fields = ['id', 'attempted_at']

# ModuleProgress Serializer
class ModuleProgressSerializer(serializers.ModelSerializer):
    module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all())
    enrollment = serializers.PrimaryKeyRelatedField(queryset=Enrollment.objects.all())

    class Meta:
        model = ModuleProgress
        fields = ['id', 'enrollment', 'module', 'is_completed']
        read_only_fields = ['id']


class CourseReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CourseReview
        fields = ['id', 'user', 'course', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user if request else None
        return super().create(validated_data)