import random
import string



from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from rest_framework.authtoken.admin import User


class FoydalanuvchiUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email manzili ko'rsatilishi shart!")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser uchun 'is_staff=True' bo'lishi shart!")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser uchun 'is_superuser=True' bo'lishi shart!")

        return self.create_user(email, password, **extra_fields)


class Foydalanuvchi(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=25, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField()
    avatar = models.ImageField(upload_to='media/avatars/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
    )

    objects = FoydalanuvchiUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Hech narsa kiritilmagan

    def str(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(Foydalanuvchi, on_delete=models.CASCADE, related_name='profile')  # 'register.Foydalanuvchi' o'rniga 'Foydalanuvchi' ishlatildi
    avatar = models.ImageField(upload_to='media/avatars/', null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)

    def str(self):
        return f"{self.user.email} - Profile"











##############################################home page

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Doctor(models.Model):
    full_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='doctors')
    description = models.TextField()
    image = models.ImageField(upload_to='doctors/')
    rating = models.FloatField(default=5.0)

    def __str__(self):
        return self.full_name

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} -> {self.doctor} ({self.time})"