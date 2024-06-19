from rest_framework import serializers
from .models import Event, Participant
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_type', 'start_time', 'end_time', 'location', 'google_meet_link', 'discount_percentage','price','final_price', 'registration_deadline']

class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    event = EventSerializer()

    class Meta:
        model = Participant
        fields = ['id', 'user', 'event', 'joined_at']
