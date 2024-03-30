from .models import Nutritionist
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction

class NutritionistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nutritionist
        fields = "__all__"

    def create(self, validated_data):
        try:
            # Verificar se já existe um usuário com o mesmo e-mail
            if get_user_model().objects.filter(email=validated_data['email']).exists():
                raise serializers.ValidationError("Error! There is already a user with the same email.")
            
            with transaction.atomic():
                # antes de inserir verificar se exite ou nao , em caso de nao criar se sim estoura um erro
                user = get_user_model().objects.create_user(
                    username=validated_data['email'],
                    email=validated_data['email'],
                    password=validated_data['password']
                )

                user.is_staff = True
                user.is_superuser = True
                user.save()
                            
                nutritionist_serializer = self.Meta.model(**validated_data)
                nutritionist_serializer.save()

            return validated_data
        except Exception as e:
            # Se ocorrer um erro, desfazer a criação do usuário
            user.delete()
            raise serializers.ValidationError(e)


