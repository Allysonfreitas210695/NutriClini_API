from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import MessageClini
from .serializers import MessageCliniSerializer

class MessageCliniViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = MessageClini.objects.all()
    serializer_class = MessageCliniSerializer

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
