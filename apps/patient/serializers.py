from .models import Food, Meal, MealPlan, Patient
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth import get_user_model


class PatientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = "__all__"

    def create(self, validated_data):
        try:
            # Verificar se já existe um usuário com o mesmo e-mail
            if get_user_model().objects.filter(email=validated_data['email']).exists():
                raise serializers.ValidationError("Error! There is already a user with the same email.")
            
            with transaction.atomic():
                validated_data['password'] = "123mudar"
                # antes de inserir verificar se exite ou nao , em caso de nao criar se sim estoura um erro
                user = get_user_model().objects.create_user(
                    username=validated_data['email'],
                    email=validated_data['email'],
                    password=validated_data['password']
                )

                user.is_staff = True
                user.is_superuser = True
                user.save()
                            
                patient_serializer = self.Meta.model(**validated_data)
                patient_serializer.save()

            return validated_data
        except Exception as e:
            # Se ocorrer um erro, desfazer a criação do usuário
            user.delete()
            raise serializers.ValidationError(e)


class MealPlanSerializer(serializers.ModelSerializer): 
    class Meta:
        model = MealPlan
        fields = "__all__"

class MealSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Meal
        fields = "__all__"

class FoodSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Food
        fields = "__all__"
