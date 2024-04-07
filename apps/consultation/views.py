from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from .models import Consultation
from .serializers import ConsultationSerializer, ConsultationHistorySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication 
from rest_framework.decorators import action

class ConsultationPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class ConsultationViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    pagination_class = ConsultationPagination

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='nutritionist/(?P<id>\d+)')
    def by_nutritionist(self, request, id=None, *args, **kwargs):
        consultation = Consultation.objects.filter(nutritionist=id)
        page = self.paginate_queryset(consultation)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='patient/(?P<id>\d+)')
    def by_patient(self, request, id=None, *args, **kwargs):
        consultation = Consultation.objects.filter(user_patient=id)
        page = self.paginate_queryset(consultation)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='status/(?P<status>\w+)')
    def by_status(self, request, status=None, *args, **kwargs):
        consultation = Consultation.objects.filter(status=status)
        page = self.paginate_queryset(consultation)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)
