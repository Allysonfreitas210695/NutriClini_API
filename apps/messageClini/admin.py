from django.contrib import admin
from .models import MessageClini

class MessageCliniAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'message', 'created_at', 'updated_at']
    list_filter = ['user', 'message']
    search_fields = ['message', 'user']  # Ajuste conforme seus campos

admin.site.register(MessageClini, MessageCliniAdmin)
