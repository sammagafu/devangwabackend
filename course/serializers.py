from rest_framework import serializers
from .models import Course, Module, Video, Document, Quiz, Question, Answer, Enrollment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'price', 'instructor','discount_percentage', 'slug', 'final_price', 'created_at', 'updated_at', 'modules']

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'title', 'course', 'order', 'videos', 'documents', 'quizzes']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'module', 'video_url']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'module', 'document_file']

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'module', 'description', 'pass_mark', 'total_marks', 'time_limit', 'questions']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'text', 'explanation', 'answers']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'question', 'text', 'is_correct']

class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at']
