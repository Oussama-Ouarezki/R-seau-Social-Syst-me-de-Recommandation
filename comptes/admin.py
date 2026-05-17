from django.contrib import admin
from .models import Profile, Interest

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']
    search_fields = ['user__username', 'user__email']

@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
