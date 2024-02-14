from django.contrib import admin
from .models import PatientConsultation

class PatientConsultationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_pacient', 'adress_consulta', 'date_Consulta', 'created_at', 'updated_at']

admin.site.register(PatientConsultation, PatientConsultationAdmin)