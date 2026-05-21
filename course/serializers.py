from rest_framework import serializers
from .models import (
    Course, Module, Video, Document, Quiz, Question, Answer, Enrollment,
    VideoProgress, DocumentProgress, QuizAttempt, ModuleProgress, FAQ, Tags, CourseReview,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']


class TagsSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(source='name', read_only=True)

    class Meta:
        model = Tags
        fields = ['id', 'tag']


class FAQSerializer(serializers.ModelSerializer):
    is_asked_by = UserSerializer(read_only=True)
    is_answered_by = UserSerializer(read_only=True)

    class Meta:
        model = FAQ
        fields = [
            'id', 'course', 'question', 'answer',
            'is_answered', 'is_asked_by', 'is_answered_by',
        ]
        read_only_fields = ['id', 'is_asked_by', 'is_answered_by']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text', 'is_correct']
        read_only_fields = ['id']


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'answers']
        read_only_fields = ['id']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'questions']
        read_only_fields = ['id']


class VideoSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(source='url')

    class Meta:
        model = Video
        fields = ['id', 'title', 'video_url', 'duration']
        read_only_fields = ['id']


class DocumentSerializer(serializers.ModelSerializer):
    document_file = serializers.FileField(source='file')

    class Meta:
        model = Document
        fields = ['id', 'title', 'document_file']
        read_only_fields = ['id']


class ModuleSerializer(serializers.ModelSerializer):
    videos = VideoSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)
    lectures = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = [
            'id', 'title', 'order', 'total_videos', 'total_documents', 'total_quizzes',
            'videos', 'documents', 'quizzes', 'lectures',
        ]
        read_only_fields = ['id', 'total_videos', 'total_documents', 'total_quizzes']

    def get_lectures(self, obj):
        lectures = []
        for video in obj.videos.all():
            minutes = video.duration // 60 if video.duration else 0
            seconds = video.duration % 60 if video.duration else 0
            lectures.append({
                'title': video.title,
                'time': f'{minutes}m {seconds}s' if video.duration else 'N/A',
                'isPremium': True,
                'video_url': video.url,
            })
        for document in obj.documents.all():
            lectures.append({
                'title': document.title,
                'time': 'Document',
                'isPremium': True,
                'document_file': document.file.url if document.file else None,
            })
        for quiz in obj.quizzes.all():
            lectures.append({
                'title': quiz.title,
                'time': 'Quiz',
                'isPremium': True,
            })
        return lectures

    def create(self, validated_data):
        validated_data['course_id'] = self.context['course_id']
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    instructor = UserSerializer(read_only=True)
    modules = ModuleSerializer(many=True, read_only=True)
    faqs = FAQSerializer(many=True, read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    cover = serializers.SerializerMethodField()
    price = serializers.DecimalField(source='final_price', max_digits=10, decimal_places=2, read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    discount_deadline = serializers.SerializerMethodField()
    is_featured = serializers.SerializerMethodField()
    total_modules = serializers.SerializerMethodField()
    total_videos = serializers.SerializerMethodField()
    total_documents = serializers.SerializerMethodField()
    total_quizzes = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'slug', 'description', 'instructor', 'final_price', 'price',
            'ispublished', 'cover', 'created_at', 'updated_at',
            'discount_percentage', 'discount_deadline', 'total_modules',
            'total_videos', 'total_documents', 'total_quizzes', 'tags', 'is_featured',
            'modules', 'faqs', 'reviews', 'rating', 'student',
        ]
        read_only_fields = [
            'id', 'slug', 'instructor', 'created_at', 'updated_at', 'final_price',
            'total_modules', 'total_videos', 'total_documents', 'total_quizzes',
            'modules', 'reviews', 'rating', 'student',
        ]

    def get_cover(self, obj):
        return None

    def get_discount_percentage(self, obj):
        return '0'

    def get_discount_deadline(self, obj):
        return None

    def get_is_featured(self, obj):
        return False

    def get_total_modules(self, obj):
        return obj.modules.count()

    def get_total_videos(self, obj):
        return sum(m.videos.count() for m in obj.modules.all())

    def get_total_documents(self, obj):
        return sum(m.documents.count() for m in obj.modules.all())

    def get_total_quizzes(self, obj):
        return sum(m.quizzes.count() for m in obj.modules.all())

    def get_reviews(self, obj):
        return obj.reviews.filter(visible=True).count()

    def get_rating(self, obj):
        visible = obj.reviews.filter(visible=True)
        if not visible.exists():
            return 0
        return round(sum(r.rating for r in visible) / visible.count(), 1)

    def get_student(self, obj):
        return obj.enrollments.count()

    def create(self, validated_data):
        faqs_data = validated_data.pop('faqs', [])
        tags_data = validated_data.pop('tags', [])
        request = self.context.get('request')
        instructor = request.user if request else None
        course = Course.objects.create(instructor=instructor, **validated_data)
        for faq_data in faqs_data:
            FAQ.objects.create(course=course, **faq_data)
        for tag_data in tags_data:
            tag_name = tag_data.get('tag') or tag_data.get('name')
            if tag_name:
                tag, _ = Tags.objects.get_or_create(name=tag_name)
                course.tags.add(tag)
        return course


class EnrollmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    last_accessed_module = serializers.SerializerMethodField()

    class Meta:
        model = Enrollment
        fields = [
            'id', 'user', 'course', 'enrolled_at', 'completion_percentage', 'is_completed',
            'started_at', 'last_accessed_module', 'progress_notes', 'certificate_issued',
        ]
        read_only_fields = [
            'id', 'user', 'course', 'enrolled_at', 'completion_percentage', 'is_completed',
            'started_at', 'last_accessed_module', 'progress_notes', 'certificate_issued',
        ]

    def get_last_accessed_module(self, obj):
        if obj.last_accessed_module:
            return {'id': obj.last_accessed_module.id, 'title': obj.last_accessed_module.title}
        return None


class VideoProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = ['id', 'video', 'watched_duration', 'is_completed']
        read_only_fields = ['id']


class DocumentProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentProgress
        fields = ['id', 'document', 'read', 'read_at']
        read_only_fields = ['id', 'read_at']


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'score', 'attempt_date']
        read_only_fields = ['id', 'attempt_date']


class ModuleProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleProgress
        fields = ['id', 'enrollment', 'module', 'completed', 'completion_date']
        read_only_fields = ['id']


class CourseReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CourseReview
        fields = ['id', 'user', 'course', 'rating', 'comment', 'created_at', 'visible']
        read_only_fields = ['id', 'user', 'created_at', 'visible']

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        validated_data['visible'] = True
        return super().create(validated_data)
