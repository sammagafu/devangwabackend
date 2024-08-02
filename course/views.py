from rest_framework import viewsets, permissions
from .models import Course, Module, Video, Document, Quiz, Question, Answer
from .serializers import CourseSerializer, ModuleSerializer, VideoSerializer, DocumentSerializer, QuizSerializer, QuestionSerializer, AnswerSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated,IsAdminUser
from rest_framework.response import Response


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    def enroll(self, request, slug=None):
        course = self.get_object()
        course.enroll(request.user)
        serializer = self.get_serializer(course)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action == 'enroll':
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()


class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        try:
            course = Course.objects.get(id=course_id)
            serializer.save(course=course)
        except Course.DoesNotExist:
            serializer.save()

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        course_id = self.request.data.get('module')
        try:
            module = Module.objects.get(id=course_id)
            serializer.save(module=module)
        except Module.DoesNotExist:
            serializer.save()

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        course_id = self.request.data.get('module')
        try:
            course = Course.objects.get(id=course_id)
            serializer.save(course=course)
        except Course.DoesNotExist:
            serializer.save()

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(module=self.request.data.get('module'))

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(quiz=self.request.data.get('quiz'))

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(question=self.request.data.get('question'))

