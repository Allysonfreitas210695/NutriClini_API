from rest_framework import serializers
from .models import Appointment, TimeSchedules

class TimeSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSchedules
        fields = "__all__"

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
        instance.date_appointments = validated_data.get('date_appointments', instance.date_appointments)
        instance.service_location = validated_data.get('service_location', instance.service_location)
        instance.save()

        # Clear existing schedules and add new ones
        instance.schedules.clear()
        for schedule_data in schedules_data:
            time_schedule, _ = TimeSchedules.objects.get_or_create(**schedule_data)
            instance.schedules.add(time_schedule)

        return instance