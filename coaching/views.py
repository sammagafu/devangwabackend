from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from .models import Event, Participant, Payment, Speaker, Schedule
from .serializers import EventSerializer, ParticipantSerializer, PaymentSerializer, SpeakerSerializer, ScheduleSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action == 'attend':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [perm() for perm in permission_classes]

    @action(detail=True, methods=['post'])
    def attend(self, request, slug=None):
        event = self.get_object()
        if event.registration_deadline < timezone.now():
            return Response({'error': 'Registration deadline has passed'}, status=400)
        participant, created = Participant.objects.get_or_create(session=event, user=request.user)
        if created:
            return Response({'status': 'Successfully joined the event'}, status=201)
        return Response({'status': 'Already registered for the event'}, status=200)

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        # Mock payment processing (replace with payment gateway)
        serializer.save(user=self.request.user, is_successful=True)

class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [IsAdminUser]

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAdminUser]