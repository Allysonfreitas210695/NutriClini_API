
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from apps.nutritionist.models import Nutritionist
from .serializers import CustomTokenObtainPairSerializer, CustomTokenRefreshSerializer

from rest_framework import status

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