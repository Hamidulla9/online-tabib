from django.contrib import admin
from .models import User, UserEducation, AdditionalUniversity, Experience, Extra_work

admin.site.register([UserEducation, AdditionalUniversity])
admin.site.register([Experience, Extra_work])
admin.site.register(User)
