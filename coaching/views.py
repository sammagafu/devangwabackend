from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser
from django.utils import timezone
from .models import Event, Participant, Payment, Speaker, Schedule
from .serializers import EventSerializer, ParticipantSerializer, PaymentSerializer, SpeakerSerializer, ScheduleSerializer
import uuid
import re

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def attend(self, request, slug=None):
        """Register the authenticated user for the event with manual payment confirmation."""
        event = self.get_object()
        user = request.user

        # Check registration deadline
        if event.registration_deadline < timezone.now():
            return Response({'detail': 'Registration deadline has passed'}, status=400)

        # Check if already registered
        if Participant.objects.filter(session=event, user=user).exists():
            return Response({'detail': 'Already registered for the event'}, status=400)

        # Free event
        if event.final_price <= 0:
            participant = Participant.objects.create(session=event, user=user)
            serializer = ParticipantSerializer(participant)
            return Response(serializer.data, status=201)

        # Handle payment confirmation
        order_tracking_id = request.data.get('order_tracking_id')
        if order_tracking_id:
            try:
                payment = Payment.objects.get(order_tracking_id=order_tracking_id, user=user, event=event)
                if payment.is_successful:
                    return Response({'detail': 'Payment already processed'}, status=400)
                # Simulate payment confirmation
                payment.is_successful = True
                payment.save()
                # Create participant
                participant = Participant.objects.create(session=event, user=user)
                serializer = ParticipantSerializer(participant)
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
                event=event,
                order_tracking_id=order_tracking_id,
                amount=event.final_price,
                currency='KES',
                is_successful=False,
                payment_method=payment_method
            )
            return Response({
                'order_tracking_id': order_tracking_id,
                'registration_pending': True,
                'instructions': f'Please confirm the {payment_method} payment to complete registration.'
            }, status=200)
        except ValidationError as e:
            return Response({'detail': str(e)}, status=400)
        except Exception as e:
            return Response({'detail': f'An error occurred: {str(e)}'}, status=500)

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

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_successful=False)

class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [IsAdminUser]

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [IsAdminUser]