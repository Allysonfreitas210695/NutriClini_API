from django.utils import timezone
from datetime import datetime, time
from rest_framework import serializers
from apps.appointments.models import Appointment, TimeSchedules
from apps.locations.models import Address
from apps.locations.serializers import AddressSerializer
from apps.patient.models import Patient
from apps.patient.serializers import PatientSerializer
from .models import Consultation, ConsultationHistory
from django.core.mail import send_mail
from django.db import transaction


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

        consultation = Consultation(
            nutritionist=validated_data.get('nutritionist'),
            patient=validated_data.get('patient'),
            address_consulta=Address.objects.get(pk=appointment.service_location.pk),
            date_Consulta=date_Consulta_aware,
            status=validated_data.get('status', 'pending')
        )

        patient_instance = validated_data.get('patient')
        patient_email = patient_instance.email 

        _patient = Patient.objects.get(pk=patient_instance.pk)
        _address = Address.objects.get(pk=appointment.service_location.pk)

        with transaction.atomic():
            consultation.save()

            send_mail(
                'Consulta Agendada',
                '',
                'nutriclinicn@gmail.com',
                [patient_email], 
                html_message=f"""
                    <html>
                    <head>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                            }}
                            .container {{
                                max-width: 600px;
                                margin: 0 auto;
                                padding: 20px;
                                border: 1px solid #ccc;
                                border-radius: 5px;
                            }}
                            h3 {{
                                color: #333;
                            }}
                            p {{
                                margin-bottom: 10px;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h3>Prezado {_patient.fullName},</h3>
                            <p>Você tem uma consulta agendada para o seguinte horário:</p>
                            <p><strong>Data e Hora:</strong> {date_Consulta_aware.strftime('%d/%m/%Y %H:%M')}</p>
                            <p><strong>Endereço:</strong> {_address.street}, {_address.city}, {_address.state}, {_address.cep}</p>
                            <br/>
                        </div>
                    </body>
                    </html>
                """,
                fail_silently=False
            )

            schedule.status = 'unavailable'
            schedule.save()

        return consultation



class ConsultationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationHistory
        fields = "__all__"