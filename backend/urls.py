from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from apps.tokenProfile.views import CustomTokenObtainPairView, CustomTokenRefreshView
from apps.appointments.views import AppointmentViewSet, TimeSchedulesViewSet
from apps.locations.views import AddressViewSet
from apps.messageClini.views import MessageCliniViewSet
from apps.consultation.views import ConsultationViewSet
from apps.profiles.views import ProfileViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter()


# Rota de cadastro de Usuarios
router.register(r'Profiles', ProfileViewSet, basename='profile')
router.register(r'Address', AddressViewSet, basename='address')
router.register(r'Appointments', AppointmentViewSet, basename='appointments')
router.register(r'TimeSchedules', TimeSchedulesViewSet, basename='timeSchedules')
router.register(r'MessageClinis', MessageCliniViewSet, basename='messageClini')
router.register(r'Consultations', ConsultationViewSet, basename='consultations')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Rota para obter o token de acesso
    path("api/token-refresh/", CustomTokenRefreshView.as_view(), name='token_refresh'),  # Rota para refresh token
    path("api/", include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
