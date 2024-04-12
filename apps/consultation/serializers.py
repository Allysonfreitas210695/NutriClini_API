from django.utils import timezone
from datetime import datetime, time
from rest_framework import serializers
from apps.appointments.models import Appointment, TimeSchedules
from apps.locations.models import Address
from apps.locations.serializers import AddressSerializer
from apps.patient.serializers import PatientSerializer
from .models import Consultation, ConsultationHistory


class ConsultationReadSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    address_consulta = AddressSerializer()

    class Meta:
        model = Consultation
        fields = ['id', 'nutritionist', 'patient', 'address_consulta', 'status', 'date_Consulta']

class ConsultationSerializer(serializers.ModelSerializer):
    appointment = serializers.IntegerField(write_only=True) 
    schedule = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Consultation
        fields = ['appointment', 'schedule', 'status', 'patient', 'nutritionist']
    
    def create(self, validated_data):
        appointment_id = validated_data.pop('appointment')
        schedule_id = validated_data.pop('schedule')

        try:
            appointment = Appointment.objects.get(pk=appointment_id)
        except Appointment.DoesNotExist:
            raise serializers.ValidationError("not existing Appointment object for Id")

        try:
            schedule = TimeSchedules.objects.get(pk=schedule_id)
        except TimeSchedules.DoesNotExist:
            raise serializers.ValidationError("not a schedule with Id")

        appointment_date = appointment.date_appointments
        schedule_time = schedule.time_value

        date_Consulta = datetime.combine(appointment_date, schedule_time)

        date_Consulta_aware = timezone.make_aware(date_Consulta)

        if Consultation.objects.filter(date_Consulta=date_Consulta_aware).exists():
            raise serializers.ValidationError("Exist in consultation for date and time.")

        consultation = Consultation.objects.create(
            nutritionist=validated_data.get('nutritionist'),
            patient=validated_data.get('patient'),
            address_consulta=Address.objects.get(pk=appointment.service_location.pk),
            date_Consulta=date_Consulta_aware,
            status=validated_data.get('status', 'pending')
        )

        schedule.status = 'unavailable'
        schedule.save()

        return consultation


class ConsultationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationHistory
        fields = "__all__"