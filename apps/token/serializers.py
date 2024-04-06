from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import serializers


class EnviarCodigoSenhaSerializer(serializers.Serializer):
        email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(max_length=30)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    id = serializers.IntegerField(read_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    type = serializers.CharField(read_only=True)
    expiry = serializers.DateTimeField(read_only=True)  # Adicionando expiry ao serializer

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['id'] = user.id
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    id = serializers.IntegerField(
        help_text="ID do perfil associado ao token de atualização."
    )
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField()
    type = serializers.CharField()
    expires = serializers.DateTimeField(read_only=True)  # Adicionando o campo de expiração

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.context['request'].user
        data['id'] = user.id
        return data