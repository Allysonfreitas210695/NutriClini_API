from rest_framework import serializers

from apps.locations.serializers import AddressSerializer
from apps.nutritionist.serializers import NutritionistSerializer
from apps.patient.serializers import PatientSerializer
from .models import Consultation, ConsultationHistory

class ConsultationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consultation
        fields = "__all__"
    

class ConsultationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationHistory
        fields = "__all__"

class CustomConsultationSerializer(serializers.ModelSerializer):
    patient = PatientSerializer()
    nutritionist = NutritionistSerializer()
    address_consulta = AddressSerializer()
    
    class Meta:
        model = Consultation
        fields = "__all__"