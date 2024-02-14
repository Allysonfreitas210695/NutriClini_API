from django.contrib import admin
from .models import Address

class AddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'cep', 'street', 'number', 'neighborhood', 'city', 'state', 'created_at', 'updated_at']
    list_filter = ['user', 'city', 'state']
    search_fields = ['full_name', 'cep', 'street', 'number', 'neighborhood', 'city', 'state']  # Ajuste conforme seus campos

admin.site.register(Address, AddressAdmin)
