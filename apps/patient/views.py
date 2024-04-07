
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Patient
from .serializers import PatientSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication 
from rest_framework.decorators import action

class PatientPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class PatientViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    pagination_class = PatientPagination

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=['get'], url_path='status/(?P<status>\w+)')
    def by_status(self, request, status=None, *args, **kwargs):
        messages = Patient.objects.filter(status=status)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data) 

    @action(detail=False, methods=['get'], url_path='nutritionist/(?P<id>\d+)')
    def by_nutritionist(self, request, id=None, *args, **kwargs):
        messages = Patient.objects.filter(nutritionist=id)
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data) 