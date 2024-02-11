from .models import Profile
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import IntegrityError

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['fullName', 'cpf', 'email', 'password', 'phone', 'specialty', 'crn', 'type']
    
    def create(self, validated_data):
        try:
            # Verificar se já existe um usuário com o mesmo e-mail
            if get_user_model().objects.filter(email=validated_data['email']).exists():
                raise serializers.ValidationError("Erro! Já existe um usuário com o mesmo e-mail.")
            
            # antes de inserir verificar se exite ou nao , em caso de nao criar se sim estoura um erro
            user = get_user_model().objects.create_user(
                username=validated_data['email'],
                email=validated_data['email'],
                password=validated_data['password']
            )

            user.is_staff = True
            user.is_superuser = True
            user.save()

            profile_serializer = self.Meta.model(user=user, **validated_data)
            profile_serializer.save()

            return validated_data
        except Exception as e:
            raise serializers.ValidationError(e)



