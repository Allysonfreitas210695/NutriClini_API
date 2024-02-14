# apps/profiles/admin.py

from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','fullName', 'cpf', 'email', 'phone', 'specialty', 'crn', 'type']
    search_fields = ['fullName', 'cpf', 'email', 'phone', 'specialty', 'crn', 'type']

admin.site.register(Profile, ProfileAdmin)
