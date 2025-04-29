from rest_framework import serializers
from .models import Event, Participant, Payment, Speaker, Schedule
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['name', 'followers', 'avatar']

class ScheduleSerializer(serializers.ModelSerializer):
    speakers = SpeakerSerializer(many=True)

    class Meta:
        model = Schedule
        fields = ['day', 'title', 'time', 'speakers']

class ParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), write_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'user', 'event', 'joined_at']
        read_only_fields = ['joined_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class PaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), write_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'event', 'amount', 'payment_date', 'is_successful']
        read_only_fields = ['payment_date', 'is_successful']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    participants = ParticipantSerializer(many=True, read_only=True, source='event')
    payments = PaymentSerializer(many=True, read_only=True)
    speakers = SpeakerSerializer(many=True, read_only=True)
    schedules = ScheduleSerializer(many=True, read_only=True)
    visitors = serializers.SerializerMethodField()
    registered = serializers.SerializerMethodField()
    attendance = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_type', 'start_time', 'end_time', 'location', 'cover',
            'discount_percentage', 'price', 'final_price', 'registration_deadline', 'discount_deadline',
            'slug', 'created_by', 'participants', 'payments', 'speakers', 'schedules', 'visitors',
            'registered', 'attendance'
        ]
        read_only_fields = ['slug', 'final_price', 'participants', 'payments', 'speakers', 'schedules',
                           'visitors', 'registered', 'attendance']

    def get_visitors(self, obj):
        return 125  # Mocked, implement view tracking

    def get_registered(self, obj):
        return obj.event.count()  # Count participants

    def get_attendance(self, obj):
        return 350  # Mocked, implement attendance tracking