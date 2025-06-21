from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
import requests
import uuid
import logging
import time

from .models import Event, Participant, Speaker, Schedule
from .serializers import EventSerializer, ParticipantSerializer, SpeakerSerializer, ScheduleSerializer

logger = logging.getLogger(__name__)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def process_payment(self, content_type_id, object_id, amount, payment_method, phone_number, card_number, auth_token):
        max_attempts = 3
        attempt = 1
        while attempt <= max_attempts:
            try:
                response = requests.post(
                    f"{settings.PAYMENT_API_BASE_URL}/checkout/",
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
                logger.error(f"Payment attempt {attempt}/{max_attempts} failed: {str(e)}")
                if attempt == max_attempts:
                    raise
                attempt += 1
                time.sleep(1)  # Wait 1 second before retrying

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def attend(self, request, slug=None):
        event = self.get_object()
        user = request.user

        if event.registration_deadline < timezone.now():
            return Response({'detail': 'Registration deadline has expired'}, status=status.HTTP_400_BAD_REQUEST)

        if Participant.objects.filter(event=event, user=user).exists():
            return Response({'detail': 'You are already registered for this event'}, status=status.HTTP_400_BAD_REQUEST)

        if event.final_price <= 0:
            participant = Participant.objects.create(event=event, user=user)
            serializer = ParticipantSerializer(participant)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        payment_method = request.data.get('payment_method', 'mpesa')
        phone_number = request.data.get('phone_number')
        card_number = request.data.get('card_number')

        try:
            content_type = ContentType.objects.get_for_model(Event)
            payment_response = self.process_payment(
                content_type_id=content_type.id,
                object_id=event.id,
                amount=event.final_price,
                payment_method=payment_method,
                phone_number=phone_number,
                card_number=card_number,
                auth_token=request.auth
            )

            if payment_response['status'] == 'succeeded':
                participant = Participant.objects.create(event=event, user=user)
                serializer = ParticipantSerializer(participant)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': payment_response.get('error', 'Payment failed')}, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({'detail': f'Payment service error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f"Attend registration error: {str(e)}")
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [IsAdminUser]

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAdminUser]