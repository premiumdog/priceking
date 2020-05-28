from django.contrib import admin
from .models import UserProfile
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'xml_link', 'credit']

admin.site.register(UserProfile, ProfileAdmin)
