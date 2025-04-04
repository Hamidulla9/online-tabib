import random
import string
from django.core.mail import send_mail
from rest_framework import serializers
from .models import Foydalanuvchi

# Tasdiqlash kodi generatsiya qilish funksiyasi
def generate_verification_code():
    return ''.join(random.choices(string.digits, k=6))

# Foydalanuvchi ro'yxatga olish serializeri
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foydalanuvchi
        fields = ['email', 'name', 'surname']

    def create(self, validated_data):
        verification_code = generate_verification_code()
        user = Foydalanuvchi.objects.create_user(**validated_data)
        user.verification_code = verification_code
        user.is_active = False  # Foydalanuvchi tasdiqlanmaguncha faol emas
        user.save()

        # Email orqali tasdiqlash kodini yuborish
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
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')

        try:
            user = Foydalanuvchi.objects.get(email=email)
            if not user.is_email_verified:
                raise serializers.ValidationError("Email tasdiqlanmagan!")

            # Login muvaffaqiyatli amalga oshdi
            return {"email": user.email}

        except Foydalanuvchi.DoesNotExist:
            raise serializers.ValidationError("Bunday foydalanuvchi mavjud emas!")

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