import random
import string
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Foydalanuvchi
from .serializers import (
    RegisterSerializer, VerifyEmailSerializer,
    EmailLoginSerializer, VerifyLoginCodeSerializer, UserProfileSerializer
)

# Ro'yxatdan o'tish (Register)
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Tasdiqlash kodi emailingizga yuborildi."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Emailni tasdiqlash (Verify Email)
class VerifyEmailAPIView(APIView):
    def post(self, request):
        serializer = VerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Email muvaffaqiyatli tasdiqlandi!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Email orqali kirish (Login)
class EmailLoginAPIView(APIView):
    def post(self, request):
        serializer = EmailLoginSerializer(data=request.data)
        if serializer.is_valid():
            verification_code = ''.join(random.choices(string.digits, k=6))
            user = get_object_or_404(Foydalanuvchi, email=serializer.validated_data['email'])
            user.verification_code = verification_code
            user.save()

            # Tasdiqlash kodini emailga yuborish
            send_mail(
                'Kirish tasdiqlash kodi',
                f'Sizning tasdiqlash kodingiz: {verification_code}',
                'admin@example.com',
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "Tasdiqlash kodi yuborildi!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login tasdiqlash (Verify Login Code)
class VerifyLoginCodeAPIView(APIView):
    def post(self, request):
        serializer = VerifyLoginCodeSerializer(data=request.data)
        if serializer.is_valid():
            user = get_object_or_404(Foydalanuvchi, email=serializer.validated_data['email'])
            user.verification_code = None  # Tasdiqlash kodini tozalash
            user.save()
            return Response({"message": "Kirish muvaffaqiyatli amalga oshirildi!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Foydalanuvchi profilini olish (Profile)
class UserProfileAPIView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
