from rest_framework import serializers
from .models import MessageClini

class MessageCliniSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageClini
        fields = '__all__'