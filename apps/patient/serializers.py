from .models import Patient
from rest_framework import serializers
from django.db import transaction

class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = "__all__"

    def create(self, validated_data):
        try:
            with transaction.atomic():        
                patient_serializer = self.Meta.model(**validated_data)
                patient_serializer.save()

            return validated_data
        except Exception as e:
            raise serializers.ValidationError(e)


