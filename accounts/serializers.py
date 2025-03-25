from rest_framework import serializers
from django.core.mail import send_mail
from .models import User, UserEducation, AdditionalUniversity, Extra_work, Experience


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
    class Meta:
        model = User
        fields = ["first_name", "last_name", "passport", "email"]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        code = user.generate_verification_code()
        send_mail(
            subject="Tasdiqlash kodi - Xavfsizlik",
            message=f"Assalomu alaykum {user},\n\n"
                    f"Sizning tasdiqlash kodingiz: {code}\n\n"
                    "Iltimos, ushbu kodni 1 daqiqa ichida kiriting.\n",
            from_email="hamidullanishonboyev9@gmail.com",
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user

    def validate_passport(self, value):
        if User.objects.filter(passport=value).exists():
            raise serializers.ValidationError("Ushbu passport allaqachon ishlatilgan.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ushbu email allaqachon ishlatilgan.")
        return value


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
