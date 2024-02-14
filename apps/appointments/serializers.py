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

    def create(self, validated_data):
        user = self.context['request'].user
        if user and user.is_authenticated:
            validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user and user.is_authenticated:
            validated_data['user'] = user
        return super().update(instance, validated_data)
