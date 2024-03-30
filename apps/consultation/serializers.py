from rest_framework import serializers
from .models import Consultation, ConsultationHistory

class ConsultationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consultation
        fields = "__all__"
    

class ConsultationHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsultationHistory
        fields = "__all__"
