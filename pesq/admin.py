from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm, ProfileForm
from .models import Linhas, CustomUser, Profile, Achievement, Paper, DashData, Experimento
# Register your models here.

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username',]

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Achievement)
admin.site.register(Linhas)
admin.site.register(Paper)
admin.site.register(DashData)
admin.site.register(Experimento)
