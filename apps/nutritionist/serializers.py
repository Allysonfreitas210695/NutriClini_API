from .models import Nutritionist
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction


# Serializer padrão para outras operações além da criação
class NutritionistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutritionist
        exclude = ['password']  # Exclua o campo de senha


class NutritionistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutritionist
        fields = "__all__"  # Inclua todos os campos para criação

    def create(self, validated_data):
        user = None  # Inicialize a variável user fora do bloco try-except
        try:
            # Verificar se já existe um usuário com o mesmo e-mail
            if get_user_model().objects.filter(email=validated_data['email']).exists():
                raise serializers.ValidationError("Error! There is already a user with the same email.")

            with transaction.atomic():
                # Crie um novo usuário associado ao nutricionista
                user = get_user_model().objects.create_user(
                    username=validated_data['email'],
                    email=validated_data['email'],
                    password=validated_data['password']
                )

                user.is_staff = True
                user.is_superuser = True
                user.save()

                # Crie o nutricionista com os dados validados, incluindo o usuário
                nutritionist_serializer = self.Meta.model(**validated_data)
                nutritionist_serializer.save()
                
            return validated_data
        except Exception as e:
            # Se ocorrer um erro, desfazer a criação do usuário se ele foi criado
            if user:
                user.delete()
            raise serializers.ValidationError(e)


