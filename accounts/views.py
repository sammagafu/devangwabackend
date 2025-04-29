from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import CustomUser, UserDetails
from .serializers import CustomUserSerializer, UserDetailsSerializer
from django.shortcuts import get_object_or_404
import json

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_serializer = CustomUserSerializer(user)
        user_details = UserDetails.objects.filter(user=user).first()
        user_details_serializer = UserDetailsSerializer(user_details) if user_details else None
        return Response({
            'user': user_serializer.data,
            'user_details': user_details_serializer.data if user_details_serializer else {}
        })

    def put(self, request):
        user = request.user

        # Handle FormData or JSON payload
        user_data = request.data.get('user')
        user_details_data = request.data.get('user_details')
        avatar_file = request.FILES.get('avatar')

        # If FormData, parse JSON strings
        if isinstance(user_data, str):
            try:
                user_data = json.loads(user_data)
            except json.JSONDecodeError:
                return Response({'non_field_errors': ['Invalid user data format']}, status=status.HTTP_400_BAD_REQUEST)
        if isinstance(user_details_data, str):
            try:
                user_details_data = json.loads(user_details_data)
            except json.JSONDecodeError:
                return Response({'non_field_errors': ['Invalid user_details data format']}, status=status.HTTP_400_BAD_REQUEST)

        # Update CustomUser
        user_serializer = CustomUserSerializer(user, data=user_data or {}, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update or create UserDetails
        user_details, created = UserDetails.objects.get_or_create(user=user)
        user_details_data = user_details_data or {}
        if avatar_file:
            user_details_data['avatar'] = avatar_file
        user_details_serializer = UserDetailsSerializer(user_details, data=user_details_data, partial=True)
        if user_details_serializer.is_valid():
            user_details_serializer.save()
        else:
            return Response(user_details_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'user': user_serializer.data,
            'user_details': user_details_serializer.data
        }, status=status.HTTP_200_OK)