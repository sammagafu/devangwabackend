from rest_framework import serializers
from .models import Event, Participant, Speaker, Schedule
from payments.serializers import PaymentSerializer
from payments.models import Payment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']

class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['name', 'avatar']

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

class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    participants = ParticipantSerializer(many=True, read_only=True, source='event')
    payments = PaymentSerializer(many=True, read_only=True)
    speakers = SpeakerSerializer(many=True, read_only=True)
    schedules = ScheduleSerializer(many=True, read_only=True)
    visitors = serializers.SerializerMethodField()
    registered = serializers.SerializerMethodField()
    attendance = serializers.SerializerMethodField()
    stream_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'event_type', 'start_time', 'end_time', 'location', 'cover',
            'discount_percentage', 'price', 'final_price', 'registration_deadline', 'discount_deadline',
            'slug', 'created_by', 'participants', 'payments', 'speakers', 'schedules', 'visitors',
            'registered', 'attendance', 'stream_url'
        ]
        read_only_fields = ['slug', 'final_price', 'participants', 'payments', 'speakers', 'schedules',
                           'visitors', 'registered', 'attendance', 'stream_url']

    def get_visitors(self, obj):
        return 125

    def get_registered(self, obj):
        return obj.event.count()

    def get_attendance(self, obj):
        return 350

    def get_stream_url(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        is_participant = Participant.objects.filter(session=obj, user=request.user).exists()
        if not is_participant:
            return None
        if obj.final_price > 0:
            has_paid = Payment.objects.filter(
                user=request.user,
                content_type__model='event',
                object_id=obj.id,
                status='succeeded'
            ).exists()
            if not has_paid:
                return None
        return obj.stream_url