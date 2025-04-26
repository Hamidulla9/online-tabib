import random
import string

from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import serializers
from .models import Foydalanuvchi, Category, Doctor, Appointment
import random
import string


# Tasdiqlash kodi generatsiya qilish funksiyasi
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

# Foydalanuvchi ro'yxatga olish serializeri
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Foydalanuvchi
        fields = ['email', 'name', 'surname', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        verification_code = generate_verification_code()

        user = Foydalanuvchi(**validated_data)
        user.set_password(password)  # Parolni hashlab saqlaymiz
        user.verification_code = verification_code
        user.is_active = False  # Email tasdiqlanmaguncha aktiv emas
        user.save()

        # Email yuborish
        send_mail(
            'Tasdiqlash kodi',
            f'Sizning tasdiqlash kodingiz: {verification_code}',
            'admin@example.com',
            [user.email],
            fail_silently=False,
        )

        return user

# Emailni tasdiqlash serializeri
class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        verification_code = attrs.get('verification_code')
        try:
            user = Foydalanuvchi.objects.get(email=email)
            if user.verification_code != verification_code:
                raise serializers.ValidationError("Tasdiqlash kodi noto‘g‘ri!")
            user.is_active = True
            user.is_email_verified = True
            user.verification_code = None
            user.save()
        except Foydalanuvchi.DoesNotExist:
            raise serializers.ValidationError("Bunday foydalanuvchi mavjud emas!")

        return attrs

# Email orqali kirish uchun serializer
from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Foydalanuvchini email va parolga qarab tekshiramiz
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Noto‘g‘ri email yoki parol!")

        # Agar foydalanuvchi emailni tasdiqlamagan bo'lsa
        if not user.is_email_verified:
            raise serializers.ValidationError("Email tasdiqlanmagan!")

        # Foydalanuvchi muvaffaqiyatli autentifikatsiya qilindi
        attrs['user'] = user
        return attrs


# Foydalanuvchi profilini olish uchun serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foydalanuvchi
        fields = ['email', 'avatar', 'is_email_verified']
        read_only_fields = ['email', 'is_email_verified']


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = Foydalanuvchi.objects.get(email=email)
            if not user.is_email_verified:
                raise serializers.ValidationError("Email tasdiqlanmagan!")
        except Foydalanuvchi.DoesNotExist:
            raise serializers.ValidationError("Bunday foydalanuvchi mavjud emas!")

        return attrs



class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not Foydalanuvchi.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email ro'yxatdan o'tmagan.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = Foydalanuvchi.objects.get(email=email)
        code = ''.join(random.choices(string.digits, k=6))
        user.verification_code = code
        user.save()
        # Shu yerda email jo‘natish funksiyasi bo‘ladi (mock yoki send_email funksiyasi)
        print(f"Verification code sent to {email}: {code}")
        return code


class VerifyCodeResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        code = data.get("code")
        try:
            user = Foydalanuvchi.objects.get(email=email, verification_code=code)
        except Foydalanuvchi.DoesNotExist:
            raise serializers.ValidationError("Kod noto‘g‘ri yoki email topilmadi.")
        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        new_password = self.validated_data["new_password"]
        user.set_password(new_password)
        user.verification_code = None  # kodni tozalaymiz
        user.save()
        return user





#################################################


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'full_name', 'category', 'description', 'image', 'rating']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

