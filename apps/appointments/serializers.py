from rest_framework import serializers
from .models import Appointment, TimeSchedules
from django.core.exceptions import ValidationError

class TimeSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSchedules
        fields = "__all__"


class AppointmentReadSerializer(serializers.ModelSerializer):
    schedules = TimeSchedulesSerializer(many=True, required=False)
    service_location = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = "__all__"

    def get_service_location(self, obj):
        if hasattr(obj, 'service_location'):
            return {
                'id': obj.service_location.id,
                'name': obj.service_location.full_name,
                "street": obj.service_location.street,
                "number": obj.service_location.number,
                "neighborhood": obj.service_location.neighborhood,
                "cep": obj.service_location.cep,
                "state": obj.service_location.state
            }
        return None


class AppointmentSerializer(serializers.ModelSerializer):
    schedules = TimeSchedulesSerializer(many=True, required=False)

    class Meta:
        model = Appointment
        fields = "__all__"

    def create(self, validated_data):
        schedules_data = validated_data.pop('schedules', [])
        appointment = Appointment.objects.create(**validated_data)
        for schedule_data in schedules_data:
            time_schedule, created = TimeSchedules.objects.get_or_create(**schedule_data)
            appointment.schedules.add(time_schedule)
        return appointment

    def update(self, instance, validated_data):
        schedules_data = validated_data.pop('schedules', [])
        existing_schedules = instance.schedules.all()

        # Criar um dicionário de horários existentes para facilitar a correspondência
        existing_schedules_dict = {schedule.id: schedule for schedule in existing_schedules}

        for schedule_data in schedules_data:
            schedule_id = schedule_data.get('id')
            if schedule_id in existing_schedules_dict:
                # Se o ID estiver presente e corresponder a um agendamento existente, atualize-o
                schedule_instance = existing_schedules_dict[schedule_id]
                schedule_instance.time_value = schedule_data.get('time_value', schedule_instance.time_value)
                schedule_instance.status = schedule_data.get('status', schedule_instance.status)
                schedule_instance.save()
            else:
                # Caso contrário, verifique se existe um agendamento com a mesma hora
                existing_schedule = existing_schedules.filter(time_value=schedule_data['time_value']).first()
                if existing_schedule:
                    # Se um agendamento com a mesma hora existir, atualize-o em vez de criar um novo
                    existing_schedule.status = schedule_data.get('status', existing_schedule.status)
                    existing_schedule.save()
                else:
                    # Caso contrário, crie um novo agendamento
                    new_schedule = TimeSchedules.objects.create(**schedule_data)
                    instance.schedules.add(new_schedule)

        # Atualizar os outros campos do agendamento
        instance.date_appointments = validated_data.get('date_appointments', instance.date_appointments)
        instance.service_location = validated_data.get('service_location', instance.service_location)
        instance.save()

        return instance
