from rest_framework import serializers
from .models import CustomUser, UserDetails
from course.serializers import CourseSerializer, EnrollmentSerializer
from coaching.serializers import PaymentSerializer, ParticipantSerializer
from community.serializers import ThreadSerializer

class UserDetailsSerializer(serializers.ModelSerializer):
    avatar = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = UserDetails
        fields = ['bio', 'is_approved', 'avatar', 'twitter', 'facebook', 'instagram', 'website']

    def validate_avatar(self, value):
        if value:
            if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise serializers.ValidationError('Avatar must be a PNG or JPEG image')
            if value.size > 2 * 1024 * 1024: # 2MB limit
                raise serializers.ValidationError('Avatar file size must be less than 2MB')
        return value

class CustomUserSerializer(serializers.ModelSerializer):
    user_details = UserDetailsSerializer(source='userdetails', read_only=True)
    courses_instructed = CourseSerializer(many=True, read_only=True, source='course_creator')
    payments = PaymentSerializer(many=True, read_only=True, source='payment_set')
    enrollments = EnrollmentSerializer(many=True, read_only=True, source='enrol')
    threads = ThreadSerializer(many=True, read_only=True, source='thread_set')
    participants = ParticipantSerializer(many=True, read_only=True, source='participant_set')

    class Meta:
        model = CustomUser
        fields = [
            'id', 'email', 'full_name', 'phonenumber', 'is_individual', 'is_company',
            'is_staff', 'is_active', 'created_at', 'user_details', 'courses_instructed',
            'payments', 'enrollments', 'threads', 'participants'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }

class CustomUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'phonenumber', 'password', 'is_individual', 'is_company')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            phonenumber=validated_data['phonenumber'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            is_individual=validated_data.get('is_individual', False),
            is_company=validated_data.get('is_company', False)
        )
        return user