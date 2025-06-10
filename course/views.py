from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action  # Corrected import
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Prefetch
from django.contrib.contenttypes.models import ContentType
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from django.conf import settings
import uuid
import logging

from .models import Course, Module, Video, Document, Quiz, Question, Answer, Enrollment, VideoProgress, DocumentProgress, QuizAttempt, ModuleProgress, FAQ, Tags,CourseReview
from .serializers import (
    CourseSerializer, ModuleSerializer, VideoSerializer, DocumentSerializer,
    QuizSerializer, QuestionSerializer, AnswerSerializer, EnrollmentSerializer,
    VideoProgressSerializer, DocumentProgressSerializer, QuizAttemptSerializer,
    ModuleProgressSerializer, FAQSerializer, TagsSerializer,CourseReviewSerializer
)

logger = logging.getLogger(__name__)

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
    def process_payment(self, content_type_id, object_id, amount, payment_method, phone_number, card_number, auth_token):
        try:
            response = requests.post(
                f"{settings.PAYMENT_API_BASE_URL}checkout/",
                json={
                    'content_type_id': content_type_id,
                    'object_id': object_id,
                    'amount': float(amount),
                    'payment_method': payment_method,
                    'phone_number': phone_number,
                    'card_number': card_number,
                    'idempotency_key': str(uuid.uuid4())
                },
                headers={'Authorization': f'Bearer {auth_token}'}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Payment request error: {str(e)}")
            raise

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def enroll(self, request, slug=None):
        course = self.get_object()
        user = request.user

        if Enrollment.objects.filter(user=user, course=course).exists():
            return Response({'detail': 'Already enrolled'}, status=status.HTTP_400_BAD_REQUEST)

        if course.final_price <= 0:
            enrollment = Enrollment.objects.create(user=user, course=course)
            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        payment_method = request.data.get('payment_method', 'mpesa')
        phone_number = request.data.get('phone_number')
        card_number = request.data.get('card_number')

        try:
            content_type = ContentType.objects.get_for_model(Course)
            payment_response = self.process_payment(
                content_type_id=content_type.id,
                object_id=course.id,
                amount=course.final_price,
                payment_method=payment_method,
                phone_number=phone_number,
                card_number=card_number,
                auth_token=request.auth
            )

            if payment_response['status'] == 'succeeded':
                enrollment = Enrollment.objects.create(user=user, course=course)
                serializer = EnrollmentSerializer(enrollment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': payment_response.get('detail', 'Payment failed')}, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({'detail': f'Payment service error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Enroll error: {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def enrolled(self, request):
        enrollments = Enrollment.objects.filter(user=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_progress(self, request, slug=None):
        course = self.get_object()
        enrollment = Enrollment.objects.filter(course=course, user=request.user).first()
        if not enrollment:
            return Response({'detail': 'Not enrolled'}, status=status.HTTP_404_NOT_FOUND)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user_progress(self, request):
        user = request.user
        enrollments = Enrollment.objects.filter(user=user).select_related('course').prefetch_related(
            Prefetch('course__modules', queryset=Module.objects.all())
        )
        enrolled_courses = []
        completed_courses = []
        for enrollment in enrollments:
            course_data = CourseSerializer(enrollment.course).data
            course_data['enrollment'] = EnrollmentSerializer(enrollment).data
            enrolled_courses.append(course_data)
            if enrollment.is_completed:
                completed_courses.append(course_data)

        documents_read = DocumentProgress.objects.filter(user=user, read=True).select_related('document')
        documents_read_data = [
            {'id': dp.document.id, 'title': dp.document.title, 'read_at': dp.read_at}
            for dp in documents_read
        ]

        quizzes_done = QuizAttempt.objects.filter(user=user).select_related('quiz')
        quizzes_done_data = QuizAttemptSerializer(quizzes_done, many=True).data

        response_data = {
            'enrolled_courses': enrolled_courses,
            'completed_courses': completed_courses,
            'documents_read': documents_read_data,
            'quizzes_done': quizzes_done_data,
        }
        return Response(response_data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def drafts(self, request):
        drafts = Course.objects.filter(instructor=request.user, ispublished=False)
        serializer = CourseSerializer(drafts, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ['enroll', 'enrolled', 'my_progress', 'user_progress', 'drafts']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [perm() for perm in permission_classes]

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        course_id = self.request.data.get('course') or self.request.query_params.get('course')
        if course_id:
            context['course_id'] = course_id
        return context

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='bulk_create')
    def bulk_create(self, request):
        course_id = request.data.get('course')
        modules_data = request.data.get('modules', [])
        created_modules = []

        for module_data in modules_data:
            if module_data.get('id'):
                continue

            serializer = self.get_serializer(data=module_data, context={'course_id': course_id})
            serializer.is_valid(raise_exception=True)
            module = serializer.save()
            created_modules.append(serializer.data)

        return Response(created_modules, status=status.HTTP_201_CREATED)

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        module_id = self.request.data.get('module')
        if not module_id:
            raise ValidationError("Module ID is required")
        try:
            module = Module.objects.get(id=module_id)
            serializer.save(module=module)
            module.total_videos = module.videos.count()
            module.save()
        except Module.DoesNotExist:
            raise ValidationError("Module does not exist")

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_progress(self, request, pk=None):
        video = self.get_object()
        progress, created = VideoProgress.objects.get_or_create(user=request.user, video=video)
        serializer = VideoProgressSerializer(progress, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201 if created else 200)
        return Response(serializer.errors, status=400)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'update_progress':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [perm() for perm in permission_classes]

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        module_id = self.request.data.get('module')
        if not module_id:
            raise ValidationError("Module ID is required")
        try:
            module = Module.objects.get(id=module_id)
            serializer.save(module=module)
            module.total_documents = module.documents.count()
            module.save()
        except Module.DoesNotExist:
            raise ValidationError("Module does not exist")

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_progress(self, request, pk=None):
        document = self.get_object()
        progress, created = DocumentProgress.objects.get_or_create(user=request.user, document=document)
        serializer = DocumentProgressSerializer(progress, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201 if created else 200)
        return Response(serializer.errors, status=400)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'update_progress':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [perm() for perm in permission_classes]

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def perform_create(self, serializer):
        module_id = self.request.data.get('module')
        if not module_id:
            raise ValidationError("Module ID is required")
        try:
            module = Module.objects.get(id=module_id)
            serializer.save(module=module)
            module.total_quizzes = module.quizzes.count()
            module.save()
        except Module.DoesNotExist:
            raise ValidationError("Module does not exist")

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def attempt(self, request, pk=None):
        quiz = self.get_object()
        serializer = QuizAttemptSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user, quiz=quiz)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'attempt':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [perm() for perm in permission_classes]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_create(self, serializer):
        quiz_id = self.request.data.get('quiz')
        if not quiz_id:
            raise ValidationError("Quiz ID is required")
        try:
            quiz = Quiz.objects.get(id=quiz_id)
            serializer.save(quiz=quiz)
        except Quiz.DoesNotExist:
            raise ValidationError("Quiz does not exist")

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [perm() for perm in permission_classes]

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer):
        question_id = self.request.data.get('question')
        if not question_id:
            raise ValidationError("Question ID is required")
        try:
            question = Question.objects.get(id=question_id)
            serializer.save(question=question)
        except Question.DoesNotExist:
            raise ValidationError("Question does not exist")

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [perm() for perm in permission_classes]

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        if not course_id:
            raise ValidationError("Course ID is required")
        try:
            course = Course.objects.get(id=course_id)
            serializer.save(course=course, is_asked_by=self.request.user)
        except Course.DoesNotExist:
            raise ValidationError("Course does not exist")

    def perform_update(self, serializer):
        serializer.save(is_answered_by=self.request.user if serializer.validated_data.get('is_answered') else None)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [perm() for perm in permission_classes]

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [perm() for perm in permission_classes]

class ModuleProgressViewSet(viewsets.ModelViewSet):
    queryset = ModuleProgress.objects.all()
    serializer_class = ModuleProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        enrollment_id = self.request.data.get('enrollment')
        module_id = self.request.data.get('module')
        if not (enrollment_id and module_id):
            raise ValidationError("Enrollment and module IDs are required")
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id, user=self.request.user)
            module = Module.objects.get(id=module_id)
            serializer.save(enrollment=enrollment, module=module)
        except (Enrollment.DoesNotExist, Module.DoesNotExist):
            raise ValidationError("Invalid enrollment or module")
        

class CourseReviewViewSet(viewsets.ModelViewSet):
    queryset = CourseReview.objects.all()
    serializer_class = CourseReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        if not course_id:
            raise ValidationError("Course ID is required")
        try:
            course = Course.objects.get(id=course_id)
            serializer.save(user=self.request.user, course=course)
        except Course.DoesNotExist:
            raise ValidationError("Course does not exist")

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return [perm() for perm in permission_classes]
    def perform_update(self, serializer):
        if 'rating' in serializer.validated_data:
            serializer.save(user=self.request.user)
        else:
            raise ValidationError("Rating is required for updating a review")