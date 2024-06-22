from rest_framework import serializers
from .models import Course, Module, Video, Document, Quiz, Question, Answer, Enrollment
from django.contrib.auth import get_user_model

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'
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

class CourseSerializer(serializers.ModelSerializer):
    course_creator = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'title','ispublished','cover', 'description', 'price', 'course_creator','discount_percentage', 'slug', 'final_price', 'created_at', 'updated_at', 'modules']
        

class EnrollmentSerializer(serializers.ModelSerializer):
    enrolleduser = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    course = CourseSerializer()

    class Meta:
        model = Enrollment
        fields = ['id', 'enrolleduser', 'course', 'enrolled_at']

