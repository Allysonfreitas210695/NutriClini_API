
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from .models import Food, Meal, MealPlan, Patient
from .serializers import FoodSerializer, MealPlanSerializer, MealSerializer, PatientSerializer
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
        page = self.paginate_queryset(messages)  # Aplicando paginação
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='nutritionist/(?P<id>\d+)')
    def by_nutritionist(self, request, id=None, *args, **kwargs):
        messages = Patient.objects.filter(nutritionist=id)
        page = self.paginate_queryset(messages)  # Aplicando paginação
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data) if page is not None else Response(serializer.data)


class MealPlanPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100
    
class MealPlanViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = MealPlan.objects.all()
    serializer_class = MealPlanSerializer
    pagination_class = MealPlanPagination

class MealPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class MealViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    pagination_class = MealPagination

class FoodPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class FoodViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    pagination_class = FoodPagination