from django.contrib import admin
from .models import MessageClini

class MessageCliniAdmin(admin.ModelAdmin):
    list_display = ['id', 'nutritionist', 'message', 'created_at', 'updated_at']
    list_filter = ['nutritionist', 'message']
    search_fields = ['message', 'user']  # Ajuste conforme seus campos

admin.site.register(MessageClini, MessageCliniAdmin)
