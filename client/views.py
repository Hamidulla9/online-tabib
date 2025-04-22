import random
import string

from dj_rest_auth.serializers import LoginSerializer
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, filters  # ✅ bu yerda filters DRFdan
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Doctor, Category, Appointment
from .serializers import (
    RegisterSerializer, VerifyEmailSerializer,
    UserProfileSerializer, EmailLoginSerializer, EmailSerializer,
    VerifyCodeResetPasswordSerializer, CategorySerializer,
    DoctorSerializer, AppointmentSerializer,
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
class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Tizimga muvaffaqiyatli kirdingiz!", "email": serializer.validated_data['email']}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# Foydalanuvchi profilini olish (Profile)
class UserProfileAPIView(APIView):
    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

class EmailLoginView(APIView):
    def post(self, request):
        serializer = EmailLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Login muvaffaqiyatli!"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class SendResetCodeView(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Kod emailga yuborildi."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeResetPasswordView(APIView):
    def post(self, request):
        serializer = VerifyCodeResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Parol muvaffaqiyatli o‘zgartirildi."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








#####################################


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name', 'description', 'category__name']  # qo'shimcha

class AppointmentCreateView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

