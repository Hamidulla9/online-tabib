from django.contrib import admin
from .models import User, UserEducation, AdditionalUniversity

admin.site.register([UserEducation, AdditionalUniversity])



@admin.register(User)
class UserViewAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'passport', 'email',]