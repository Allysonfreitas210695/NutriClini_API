from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['id'] = user.id
        return data

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()
    id = serializers.IntegerField(
        help_text="ID do perfil associado ao token de atualização."
    )
    type = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.context['request'].user
        data['id'] = user.id
        return data
