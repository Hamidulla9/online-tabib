from rest_framework import serializers
from django.core.mail import send_mail
from .models import User, UserEducation, AdditionalUniversity, Extra_work, Experience
from django.contrib.auth import authenticate


class Extra_workSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra_work
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    experience = Extra_workSerializer(many=True, required=False)

    class Meta:
        model = Experience
        fields = '__all__'

    def create(self, validated_data):
        additional_universities_data = self.context['request'].data.get('additional_universities', [])
        experiences = Experience.objects.create(**validated_data)

        for university_data in additional_universities_data:
            Extra_work.objects.create(user_education=experiences, **university_data)

        return experiences


class AdditionalUniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalUniversity
        fields = '__all__'


class UserEducationSerializer(serializers.ModelSerializer):
    additional_universities = AdditionalUniversitySerializer(many=True, required=False)

    class Meta:
        model = UserEducation
        fields = '__all__'

    def create(self, validated_data):
        additional_universities_data = self.context['request'].data.get('additional_universities', [])
        user_education = UserEducation.objects.create(**validated_data)

        for university_data in additional_universities_data:
            AdditionalUniversity.objects.create(user_education=user_education, **university_data)

        return user_education


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "passport", "email", "password"]

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Parol uzunligi 8 yoki undan kop bo'lishi kerak.")
        if sum(c.isdigit() for c in value) < 1:
            raise serializers.ValidationError("Parolda kamida 1 ta raqam bo'lishi kerak.")
        if sum(c.isalpha() for c in value) < 2:
            raise serializers.ValidationError("Parolda kamida 2 ta harf bo'lishi kerak.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        code = user.generate_verification_code()
        send_mail(
            subject="Tasdiqlash kodi - Xavfsizlik",
            message=f"Assalomu alaykum {user.first_name},\n\n"
                    f"Sizning tasdiqlash kodingiz: {code}\n\n"
                    "Iltimos, ushbu kodni 1 daqiqa ichida kiriting.\n",
            from_email="hamidullanishonboyev9@gmail.com",
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if user is None:
            raise serializers.ValidationError({
                "non_field_errors": "Email yoki parol noto‘g‘ri. Parolni unutdingizmi?"
            })

        data['user'] = user
        return data


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Bunday foydalanuvchi yo‘q")

        if user.verification_code != data["code"]:
            raise serializers.ValidationError("Tasdiqlash kodi noto‘g‘ri")

        user.is_active = True
        user.verification_code = None
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bunday email topilmadi.")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        code = user.generate_verification_code()
        send_mail(
            subject="Parolni tiklash",
            message=f"Parolni tiklash uchun tasdiqlash kodingiz: {code}",
            from_email="hamidullanishonboyev9@gmail.com",
            recipient_list=[email],
            fail_silently=False,
        )


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Parol uzunligi 8 yoki undan kop bo'lishi kerak.")
        if sum(c.isdigit() for c in value) < 1:
            raise serializers.ValidationError("Parolda kamida 1 ta raqam bo'lishi kerak.")
        if sum(c.isalpha() for c in value) < 2:
            raise serializers.ValidationError("Parolda kamida 2 ta harf bo'lishi kerak.")
        return value

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Email topilmadi.")

        if user.verification_code != data['code']:
            raise serializers.ValidationError("Tasdiqlash kodi noto‘g‘ri.")

        return data

    def save(self):
        user = User.objects.get(email=self.validated_data['email'])
        user.set_password(self.validated_data['new_password'])
        user.verification_code = None
        user.save()
        return user
