from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication 
from .models import Appointment, TimeSchedules
from .serializers import AppointmentSerializer
from rest_framework.decorators import action

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
        if serializer.is_valid():
            appointment = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='nutritionist/(?P<id>\d+)')
    def by_nutritionist(self, request, id=None, *args, **kwargs):
        appointments = Appointment.objects.filter(nutritionist=id)
        page = self.paginate_queryset(appointments)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)
