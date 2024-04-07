
import random
import string
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from apps.nutritionist.models import Nutritionist
from apps.patient.models import Patient
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, EnviarCodigoSenhaSerializer, ResetPasswordSerializer
from rest_framework import status
from rest_framework import status
from django.core.mail import send_mail
from decouple import config
from rest_framework.views import APIView
from decouple import config
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import NotFound

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtendo o token de acesso
        token = response.data.get('access')

        # Verificando se o token é válido
        if token:
            # Decodificando o token para obter a data de expiração
            from rest_framework_simplejwt.tokens import AccessToken
            token_object = AccessToken(token)
            expiry_date = token_object['exp']

            # Adicionando a data de expiração ao retorno
            response.data['expiry'] = expiry_date

        # Definindo id como None por padrão
        response.data['id'] = None

        # Verificando se o usuário é um nutricionista
        if Nutritionist.objects.filter(email=request.data["username"]).exists():
            try:
                profile = Nutritionist.objects.get(email=request.data["username"])
                response.data['id'] = profile.id
                response.data['type'] = "Nutritionist"
            except Nutritionist.DoesNotExist:
                pass
        # Verificando se o usuário é um paciente
        elif Patient.objects.filter(email=request.data["username"]).exists():
            try:
                profile = Patient.objects.get(email=request.data["username"])
                response.data['id'] = profile.id
                response.data['type'] = "Patient"
            except Patient.DoesNotExist:
                pass

        # Se o id ainda for None, nenhum perfil foi encontrado, então lança uma exceção
        if response.data['id'] is None:
            raise serializers.ValidationError("No profile found for the provided email.")

        return response

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = CustomTokenRefreshSerializer 

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')  # Extrai o refresh token da requisição
        id = request.data.get('id')  # Extrai o ID do perfil da requisição

        # Verificar se o refresh_token e o id foram fornecidos
        if not refresh_token or not id:
            return Response(
                {'detail': 'Both refresh token and profile ID are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Chamada ao método post da classe base para obter a resposta padrão
        response = super().post(request, *args, **kwargs)

        try:
            profile_type = request.data.get("type")
            if profile_type == "Nutritionist" and Nutritionist.objects.filter(id=id).exists():
                nutritionist = Nutritionist.objects.get(id=id)
                # Adicionar o ID e o tipo do perfil à resposta
                response.data['id'] = nutritionist.id
                response.data['type'] = "Nutritionist"
            elif profile_type == "Patient" and Patient.objects.filter(id=id).exists():
                patient = Patient.objects.get(id=id)
                # Adicionar o ID e o tipo do perfil à resposta
                response.data['id'] = patient.id
                response.data['type'] = "Patient"
            else:
                # Se o tipo não for reconhecido ou o perfil não for encontrado, retorne uma resposta de erro
                return Response(
                    {'detail': f'Profile not found for the given ID or incorrect type "{profile_type}".'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except NotFound as e:
            # Se o perfil não for encontrado, retorne uma resposta de erro
            return Response(
                {'detail': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Adicionando o campo de expiração à resposta
        access_token = response.data.get('access')
        if access_token:
            from rest_framework_simplejwt.tokens import AccessToken
            access_token_obj = AccessToken(access_token)
            response.data['expires'] = access_token_obj['exp']

        # Adicionar o refresh token à resposta
        response.data['refresh'] = refresh_token

        return response


class EnviarCodigoSenhaAPIView(APIView):
    
     def post(self, request, *args, **kwargs):
        serializer = EnviarCodigoSenhaSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            user_type = serializer.validated_data.get('type')

            if user_type == 'Nutritionist' and Nutritionist.objects.filter(email=email).exists():
                user = Nutritionist.objects.get(email=email)
            elif user_type == 'Patient' and Patient.objects.filter(email=email).exists():
                user = Patient.objects.get(email=email)
            else:
                return Response({'mensagem': 'Nenhum usuário encontrado com este endereço de email ou tipo'}, status=status.HTTP_400_BAD_REQUEST)

            codigo = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
            send_mail(
                'Seu código de verificação',
                f'Seu código de verificação é: {codigo}',
                'nutriclinicn@gmail.com',
                [email],
                fail_silently=False,
            )
            return Response({'codigo': codigo, 'email': user.email, 'mensagem': 'Email enviado com sucesso!'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            new_password = serializer.validated_data.get('new_password')
            user_type = serializer.validated_data.get('type')

            # Check if the type is either "Nutritionist" or "Patient"
            if user_type not in ['Nutritionist', 'Patient']:
                return Response({'message': 'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)

            if Nutritionist.objects.filter(email=email).count() == 0 and Patient.objects.filter(email=email).count() == 0:
                return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

            user.set_password(new_password)
            user.save()

            if user_type == 'Nutritionist':
                try:
                    nutritionist = Nutritionist.objects.get(email=email)
                    nutritionist.password = new_password
                    nutritionist.save()
                except Nutritionist.DoesNotExist:
                    pass
            elif user_type == 'Patient':
                try:
                    patient = Patient.objects.get(email=email)
                    patient.password = new_password
                    patient.save()
                except Patient.DoesNotExist:
                    pass

            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
