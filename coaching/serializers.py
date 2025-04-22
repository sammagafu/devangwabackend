from rest_framework import serializers
from .models import Event, Participant,Payment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email','full_name']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_type', 'start_time', 'end_time', 'location', 'cover', 'discount_percentage','price','final_price', 'registration_deadline','discount_deadline','slug']
        read_only_fields = ['slug']

class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer()

    class Meta:
        model = Participant
        fields = ['id', 'user', 'event', 'joined_at']

        
class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'event', 'amount', 'payment_date', 'is_successful']