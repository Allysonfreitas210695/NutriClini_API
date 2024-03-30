from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from .models import MessageClini
from .serializers import MessageCliniSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication 
from rest_framework.decorators import action

class ProfilePagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class MessageCliniViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = MessageClini.objects.all()
    serializer_class = MessageCliniSerializer
    pagination_class = ProfilePagination

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'], url_path='nutritionist/(?P<id>\d+)')
    def by_nutritionist(self, request, id=None, *args, **kwargs):
        messageClini = MessageClini.objects.filter(nutritionist=id)
        if messageClini.exists():
            serializer = self.get_serializer(messageClini, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK) 