
import random
import string
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from apps.nutritionist.models import Nutritionist
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, EnviarCodigoSenhaSerializer, ResetPasswordSerializer
from rest_framework import status
from rest_framework import status
from django.core.mail import send_mail
from decouple import config
from rest_framework.views import APIView
from decouple import config
from django.contrib.auth.models import User

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            profile = Nutritionist.objects.get(email=request.data["username"])
            response.data['id'] = profile.id
        except Nutritionist.DoesNotExist:
            response.data['id'] = None

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
            # Tente obter o perfil pelo ID fornecido
            profile = Nutritionist.objects.get(id=id)
            # Adicionar o ID e o tipo do perfil à resposta
            response.data['id'] = profile.id
            response.data['type'] = profile.type
        except Nutritionist.DoesNotExist:
            # Se o perfil não for encontrado, retorne uma resposta de erro
            return Response(
                {'detail': 'Profile not found for the given ID'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Adicionar o refresh token à resposta
        response.data['refresh'] = refresh_token

        return response

class EnviarCodigoSenhaAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = EnviarCodigoSenhaSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')  # Get the validated email
            if Nutritionist.objects.filter(email=email).exists():
                nutritionist = Nutritionist.objects.filter(email=email).first()
                codigo = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))

                send_mail(
                    'Seu codigó de verificação',
                    f'Seu codigó de verificação é: {codigo}',
                    config('EMAIL_HOST_USER'),
                    [email],
                    fail_silently=False,
                )
                return Response({'codigo': codigo, 'nutritionist': {'email': nutritionist.email}, 'mensagem': 'Email enviado com sucesso!'})
            else:
                return Response({'mensagem': 'No nutritionist found with this email address'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            new_password = serializer.validated_data.get('new_password')

            if not email or not new_password:
                return Response({'message': 'Both email and new password are required.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

            user.set_password(new_password)
            user.save()

            try:
                nutritionist = Nutritionist.objects.get(email=email)
                nutritionist.password = new_password
                nutritionist.save()
            except Nutritionist.DoesNotExist:
                pass 

            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
