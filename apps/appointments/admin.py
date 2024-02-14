# admin.py
from django.contrib import admin
from apps.appointments.models import Appointment

class TimeSchedulesInline(admin.TabularInline):
    model = Appointment.schedules.through
    extra = 1

class AppointmentAdmin(admin.ModelAdmin):
    inlines = [TimeSchedulesInline]
    list_display = ['id', 'user', 'date_appointments', 'service_location']
    list_filter = ['date_appointments', 'service_location']
    search_fields = ['date_appointments', 'service_location']

admin.site.register(Appointment, AppointmentAdmin)