from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from .models import Consultation
from .serializers import ConsultationSerializer, ConsultationHistorySerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication 
from rest_framework.decorators import action

class ProfilePagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class ConsultationViewSet(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Consultation.objects.all()
    serializer_class = ConsultationSerializer
    pagination_class = ProfilePagination

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        @action(detail=True, methods=['GET'])
        def user_history(self, request, pk=None):
            consultation = self.get_object()
            user_id = consultation.user_patient.id
            user_history = ConsultationHistory.objects.filter(user_patient_id=user_id)
            serializer = ConsultationHistorySerializer(user_history, many=True)
            return Response(serializer.data)