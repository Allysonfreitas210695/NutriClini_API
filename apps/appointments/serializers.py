from rest_framework import serializers
from .models import Appointment, TimeSchedules

class TimeSchedulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeSchedules
        fields = "__all__"

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
