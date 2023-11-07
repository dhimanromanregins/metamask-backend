# your_app/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'custom_id', 'secret_phrase_1', 'secret_phrase_2', 'secret_phrase_3', 'secret_phrase_4', 'secret_phrase_5', 'secret_phrase_6', 'secret_phrase_7', 'secret_phrase_8', 'secret_phrase_9', 'secret_phrase_10', 'secret_phrase_11', 'secret_phrase_12')

admin.site.register(CustomUser, CustomUserAdmin)
