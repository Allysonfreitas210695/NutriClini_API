from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication 
from .models import Appointment, TimeSchedules
from .serializers import AppointmentReadSerializer, AppointmentSerializer, TimeSchedulesSerializer
from rest_framework.decorators import action
from django.core.exceptions import ValidationError as DjangoValidationError

class AppointmentPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class AppointmentViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    pagination_class = AppointmentPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            if serializer.is_valid():
                appointment = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except DjangoValidationError as e:                            
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        try:
            if serializer.is_valid():
                appointment = serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except DjangoValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['get'], url_path='nutritionist/(?P<id>\d+)')
    def by_nutritionist(self, request, id=None, *args, **kwargs):
        appointments = Appointment.objects.filter(nutritionist=id)
        page = self.paginate_queryset(appointments)
        
        # Use o serializador de leitura que inclui o campo service_location
        serializer = AppointmentReadSerializer(page, many=True, context={'include_service_location': True})
        
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)

    def get_serializer_class(self):
        # Use o serializador de leitura para respostas de consulta (GET)
        if self.action in ['list', 'retrieve']:
            return AppointmentReadSerializer
        return AppointmentSerializer

class TimeSchedulesPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class TimeSchedulesViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TimeSchedules.objects.all()
    serializer_class = TimeSchedulesSerializer
    pagination_class = TimeSchedulesPagination