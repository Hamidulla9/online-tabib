from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserEducation, AdditionalUniversity, Experience, Extra_work, User
from .serializers import RegisterSerializer, VerifyCodeSerializer, UserEducationSerializer, \
    AdditionalUniversitySerializer, ExperienceSerializer, Extra_workSerializer, UserLoginSerializer, \
    ResetPasswordSerializer, ForgotPasswordSerializer
from django.contrib.auth import login


from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserLoginSerializer
from .models import User

class LoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)

            # 👇 Backendni qo‘shamiz
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # yoki sizning backend'laringizdan biri

            login(request, user)
            return Response({"message": "Login muvaffaqiyatli bajarildi", "email": user.email},
                            status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExperienceList(generics.ListAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class ExperienceViewSet(generics.CreateAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer

class Extra_workViewSet(generics.CreateAPIView):
    queryset = Extra_work.objects.all()
    serializer_class = Extra_workSerializer


class UserEducationList(generics.ListAPIView):
    queryset = UserEducation.objects.all()
    serializer_class = UserEducationSerializer


class UserEducationViewSet(generics.CreateAPIView):
    queryset = UserEducation.objects.all()
    serializer_class = UserEducationSerializer

class AdditionalUniversityViewSet(generics.CreateAPIView):
    queryset = AdditionalUniversity.objects.all()
    serializer_class = AdditionalUniversitySerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Tasdiqlash kodi yuborildi"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeView(APIView):
    serializer_class = VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Ro‘yxatdan o‘tish tasdiqlandi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(generics.CreateAPIView):
    serializer_class = ForgotPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Tasdiqlash kodi yuborildi"}, status=200)

class ResetPasswordView(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Yangi parol yaratildi"}, status=200)
