# serializers.py

from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},  # Hide password field in responses
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
