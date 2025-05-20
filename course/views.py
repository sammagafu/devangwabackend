# course_app/views.py
from rest_framework import viewsets, permissions,generics,status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Prefetch
from .models import Course, Module, Video, Document, Quiz, Question, Answer, Enrollment, VideoProgress, DocumentProgress, QuizAttempt, ModuleProgress, FAQ, Tags, Payment
from .serializers import (
    CourseSerializer, ModuleSerializer, VideoSerializer, DocumentSerializer,
    QuizSerializer, QuestionSerializer, AnswerSerializer, EnrollmentSerializer,
    VideoProgressSerializer, DocumentProgressSerializer, QuizAttemptSerializer,
    ModuleProgressSerializer, FAQSerializer, TagsSerializer
)
import uuid
import re

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def enroll(self, request, slug=None):
        """Enroll the authenticated user in the course with manual payment confirmation."""
        course = self.get_object()
        user = request.user

        # Check if already enrolled
        if Enrollment.objects.filter(user=user, course=course).exists():
            return Response({'detail': 'Already enrolled'}, status=400)

        # Free course
        if course.final_price <= 0:
            enrollment = Enrollment.objects.create(user=user, course=course)
            serializer = EnrollmentSerializer(enrollment)
            return Response(serializer.data, status=201)

        # Handle payment confirmation
        order_tracking_id = request.data.get('order_tracking_id')
        if order_tracking_id:
            try:
                payment = Payment.objects.get(order_tracking_id=order_tracking_id, user=user, course=course)
                if payment.status == 'succeeded':
                    return Response({'detail': 'Payment already processed'}, status=400)
                # Simulate payment confirmation
                payment.status = 'succeeded'
                payment.save()
                # Create enrollment
                enrollment = Enrollment.objects.create(user=user, course=course)
                payment.enrollment = enrollment
                payment.save()
                serializer = EnrollmentSerializer(enrollment)
                return Response(serializer.data, status=201)
            except Payment.DoesNotExist:
                return Response({'detail': 'Invalid or unauthorized payment'}, status=400)
            except Exception as e:
                return Response({'detail': f'Error confirming payment: {str(e)}'}, status=500)

        # Initiate payment
        try:
            phone_number = request.data.get('phone_number')
            card_number = request.data.get('card_number')
            payment_method = request.data.get('payment_method', 'mpesa')
            if payment_method not in ['mpesa', 'vodacom', 'airtel', 'mtn', 'card']:
                raise ValidationError("Invalid payment method")
            if payment_method == 'card' and not card_number:
                raise ValidationError("Card number is required for card payments")
            if payment_method != 'card' and not phone_number:
                raise ValidationError("Phone number is required for mobile payments")
            if phone_number and not re.match(r'^\+254\d{9}$', phone_number):
                raise ValidationError("Invalid phone number format. Use +254 followed by 9 digits.")
            if card_number and not re.match(r'^\d{16}$', card_number):
                raise ValidationError("Invalid card number format. Use 16 digits.")
            order_tracking_id = str(uuid.uuid4())
            # Create pending payment
            Payment.objects.create(
                user=user,
                course=course,
                order_tracking_id=order_tracking_id,
                amount=course.final_price,
                currency='KES',
                status='pending',
                payment_method=payment_method
            )
            return Response({
                'order_tracking_id': order_tracking_id,
                'enrollment_pending': True,
                'instructions': f'Please confirm the {payment_method} payment to complete enrollment.'
            }, status=200)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=400)
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=500)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def enrolled(self, request):
        """Return a list of enrollments for the authenticated user."""
        enrollments = Enrollment.objects.filter(user=request.user)
        serializer = EnrollmentSerializer(enrollments, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_progress(self, request, slug=None):
        """Return the authenticated user's progress in the course."""
        course = self.get_object()
        enrollment = Enrollment.objects.filter(course=course, user=request.user).first()
        if not enrollment:
            return Response({'detail': 'Not enrolled'}, status=404)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def user_progress(self, request):
        """Return enrolled courses, completed courses, documents read, and quizzes done for the user."""
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
        """Return a list of unpublished (draft) courses for the authenticated user."""
        drafts = Course.objects.filter(instructor=request.user, ispublished=False)
        serializer = CourseSerializer(drafts, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action in ['enroll', 'enrolled', 'my_progress', 'user_progress']:
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()

class ModuleViewSet(viewsets.ModelViewSet):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # Pass course_id from request data or URL
        course_id = self.request.data.get('course') or self.request.query_params.get('course')
        if course_id:
            context['course_id'] = course_id
        return context

    def create(self, request, *args, **kwargs):
        # Handle single module creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        # Handle single module update
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
                # Skip modules with IDs (handled by update)
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
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action == 'update_progress':
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()

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
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action == 'update_progress':
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()

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
            self.permission_classes = [permissions.IsAdminUser]
        elif self.action == 'attempt':
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()

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
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()

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
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()

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
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()

class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()

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