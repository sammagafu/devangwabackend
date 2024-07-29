from rest_framework import serializers
from .models import Course, Module, Video, Document, Quiz, Question, Answer, Enrollment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email','full_name']
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']
        read_only_fields = ['id']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'explanation', 'answers']
        read_only_fields = ['id', 'answers']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'slug', 'description', 'pass_mark', 'total_marks', 'time_limit', 'questions']
        read_only_fields = ['id', 'questions']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'slug', 'document_file']
        read_only_fields = ['id']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'slug', 'video_url']
        read_only_fields = ['id','module']

class ModuleSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ['id', 'title', 'slug', 'order', 'description', 'videos', 'documents', 'quizzes']
        read_only_fields = ['id', 'videos', 'documents', 'quizzes']

class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    course = serializers.StringRelatedField()

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at']
        read_only_fields = ['id', 'user', 'course', 'enrolled_at']

class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    enrollments = EnrollmentSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'slug', 'description', 'instructor', 'price', 'ispublished', 'cover', 'created_at', 'updated_at', 'discount_percentage', 'discount_deadline', 'modules', 'enrollments', 'final_price']
        read_only_fields = ['id', 'modules', 'enrollments', 'final_price']


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    course = serializers.StringRelatedField()

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at']
        read_only_fields = ['id', 'user', 'course', 'enrolled_at']
