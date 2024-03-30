from django.contrib import admin
from .models import Consultation

class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'address_consulta', 'date_Consulta', 'created_at', 'updated_at']


admin.site.register(Consultation, ConsultationAdmin)
