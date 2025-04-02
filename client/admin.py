from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Foydalanuvchi, Profile

# Foydalanuvchi admini
class FoydalanuvchiAdmin(UserAdmin):
    # Standart maydonlar
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'surname', 'avatar')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_email_verified', 'verification_code')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    # Admin panelida ko'rsatiladigan maydonlar
    list_display = ('email', 'name', 'surname', 'is_email_verified', 'is_staff', 'is_active')
    list_filter = ('is_email_verified', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('email', 'name', 'surname')
    ordering = ('email',)

    # Foydalanuvchi yaratish uchun qo'shimcha parametrlar
    filter_horizontal = ('groups', 'user_permissions')


# Profile admini
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'name', 'surname')
    search_fields = ('user__email', 'name', 'surname')
    list_filter = ('user',)

# Modellarni admin panelida ro'yxatga olish
admin.site.register(Foydalanuvchi, FoydalanuvchiAdmin)
admin.site.register(Profile, ProfileAdmin)