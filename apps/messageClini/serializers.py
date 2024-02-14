from rest_framework import serializers
from .models import MessageClini

class MessageCliniSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageClini
        fields = '__all__'

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