from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.db import models
import random
from django.utils.timezone import now



class Experience(models.Model):
    ish_joyi = models.CharField(max_length=255)
    nomi = models.CharField(max_length=255)
    lavozimi = models.CharField(max_length=255)
    ishga_kirgan_yili = models.DateField()

    def __str__(self):
        return self.nomi

class Extra_work(models.Model):
    experience = models.ForeignKey(Experience, on_delete=models.CASCADE, related_name='experience')
    ish_joyi = models.CharField(max_length=255)
    nomi = models.CharField(max_length=255)
    lavozimi = models.CharField(max_length=255)
    ishga_kirgan_yili = models.DateField()

    def __str__(self):
        return self.nomi


class UserEducation(models.Model):
    oqigan_joyi = models.CharField(max_length=255)
    nomi = models.CharField(max_length=255)
    yonalish = models.CharField(max_length=255)
    diplom_raqami = models.CharField(max_length=50)
    diplom_fayli = models.FileField(upload_to='diploms/')

    def __str__(self):
        return self.oqigan_joyi

class AdditionalUniversity(models.Model):
    user_education = models.ForeignKey(UserEducation, on_delete=models.CASCADE, related_name='additional_universities')
    oqigan_joyi = models.CharField(max_length=255)
    nomi = models.CharField(max_length=255)
    yonalish = models.CharField(max_length=255)
    diplom_raqami = models.CharField(max_length=50)
    diplom_fayli = models.FileField(upload_to='diploms/')

    def __str__(self):
        return self.oqigan_joyi


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, passport, email, password=None):
        if not email:
            raise ValueError("Email kiritish majburiy")
        user = self.model(
            first_name=first_name,
            last_name=last_name,
            passport=passport,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    passport = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "passport"]

    def __str__(self):
        return self.email

    def is_valid(self):
        """Kod 1 daqiqa ichida ishlatilishi kerak"""
        return (now() - self.created_at).seconds < 60

    def generate_verification_code(self):
        code = str(random.randint(100000, 999999))
        self.verification_code = code
        self.save()
        return code
