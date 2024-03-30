
# Create your views here.
from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Nutritionist
from .serializers import NutritionistSerializer

class NutritionistPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class NutritionistViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Nutritionist.objects.all()
    serializer_class = NutritionistSerializer
    pagination_class = NutritionistPagination

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
