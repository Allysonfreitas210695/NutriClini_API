from rest_framework import serializers
from .models import Consultation, ConsultationHistory

class ConsultationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consultation
        fields = ['id', 'user_patient', 'address_consulta', 'date_Consulta', 'status']
        

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
    

class ConsultationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationHistory
        fields = ['id', 'user_patient', 'consultation', 'message', 'created_at', 'updated_at']
