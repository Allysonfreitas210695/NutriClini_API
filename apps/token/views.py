
import random
import string
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from apps.nutritionist.models import Nutritionist
from apps.nutritionist.serializers import NutritionistSerializer
from apps.patient.models import Patient
from apps.patient.serializers import PatientSerializer
from apps.token.models import CodigoReset
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer, EnviarCodigoSenhaSerializer, ResetPasswordSerializer, VerificarCodigoSerializer
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
        refresh_token = request.data.get('refresh') 
        id = request.data.get('id') 

        if not refresh_token or not id:
            return Response(
                {'detail': 'Both refresh token and profile ID are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        response = super().post(request, *args, **kwargs)

        try:
            profile_type = request.data.get("type")
            if profile_type == "Nutritionist" and Nutritionist.objects.filter(id=id).exists():
                nutritionist = Nutritionist.objects.get(id=id)
                response.data['id'] = nutritionist.id
                response.data['type'] = "Nutritionist"
            elif profile_type == "Patient" and Patient.objects.filter(id=id).exists():
                patient = Patient.objects.get(id=id)
                response.data['id'] = patient.id
                response.data['type'] = "Patient"
            else:
                return Response(
                    {'detail': f'Profile not found for the given ID or incorrect type "{profile_type}".'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except NotFound as e:
            return Response(
                {'detail': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        
        access_token = response.data.get('access')
        if access_token:
            from rest_framework_simplejwt.tokens import AccessToken
            access_token_obj = AccessToken(access_token)
            response.data['expires'] = access_token_obj['exp']

        response.data['refresh'] = refresh_token

        return response


class EnviarCodigoSenhaAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = EnviarCodigoSenhaSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')

            code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
            
            if Nutritionist.objects.filter(email=email).exists():
                nutritionist = Nutritionist.objects.get(email=email)
                CodigoReset.objects.filter(nutritionist=nutritionist).delete()
                codigo_reset = CodigoReset.objects.create(codigo=code, nutritionist=nutritionist)
            elif Patient.objects.filter(email=email).exists():
                patient = Patient.objects.get(email=email)
                CodigoReset.objects.filter(patient=patient).delete()
                codigo_reset = CodigoReset.objects.create(codigo=code, patient=patient)
            else:
                return Response({'message': 'No user found with this email address'}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                send_mail(
                    'Seu código de verificação',
                    f'Seu código de verificação é: {codigo_reset.codigo}',
                    'nutriclinicn@gmail.com',
                    [email],
                    html_message=f"""
                        <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                }}
                                .container {{
                                    max-width: 600px;
                                    margin: 0 auto;
                                    padding: 20px;
                                    border: 1px solid #ccc;
                                    border-radius: 5px;
                                }}
                                h3 {{
                                    color: #333;
                                }}
                                p {{
                                    margin-bottom: 10px;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <h3>Seu código de verificação</h3>
                                <p>Seu código de verificação é: <strong>{codigo_reset.codigo}</strong></p>
                                <p>Use este código para concluir o processo de verificação.</p>
                                <p>Obrigado,</p>
                                <p>Equipe NutriClinic</p>
                            </div>
                        </body>
                        </html>
                    """,
                    fail_silently=False
                )

            except Exception as e:
                return Response({'message': 'Failed to send verification email'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'message': 'Email sent successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class VerificarCodigoView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = VerificarCodigoSerializer(data=request.data)
        if serializer.is_valid():
            codigo = serializer.validated_data.get('codigo')

            # Verificar se o código existe no novo modelo
            if CodigoReset.objects.filter(codigo=codigo).exists():
                codigo = CodigoReset.objects.get(codigo=codigo)
                if codigo.patient is not None:
                    patient_email = codigo.patient.email
                    CodigoReset.objects.filter(patient=codigo.patient).delete()
                    return Response({'message': 'Código válido', 'type': 'Patient', 'email': patient_email}, status=status.HTTP_200_OK)
                elif codigo.nutritionist is not None:
                    nutritionist_email = codigo.nutritionist.email
                    CodigoReset.objects.filter(nutritionist=codigo.nutritionist).delete()
                    return Response({'message': 'Código válido', 'type': 'Nutritionist', 'email': nutritionist_email}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Código inválido'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(APIView):
    
    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            new_password = serializer.validated_data.get('new_password')
            type = serializer.validated_data.get('type')

            if type not in ['Nutritionist', 'Patient']:
                return Response({'message': 'Invalid user type.'}, status=status.HTTP_400_BAD_REQUEST)

            if Nutritionist.objects.filter(email=email).count() == 0 and Patient.objects.filter(email=email).count() == 0:
                return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

            user.set_password(new_password)
            user.save()

            if type == 'Nutritionist':
                try:
                    nutritionist = Nutritionist.objects.get(email=email)
                    nutritionist.password = new_password
                    nutritionist.save()
                except Nutritionist.DoesNotExist:
                    pass
            elif type == 'Patient':
                try:
                    patient = Patient.objects.get(email=email)
                    patient.password = new_password
                    patient.save()
                except Patient.DoesNotExist:
                    pass

            return Response({'message': 'Password reset successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
