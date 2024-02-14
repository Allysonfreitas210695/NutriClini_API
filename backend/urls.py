from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.appointments.views import AppointmentViewSet, TimeSchedulesViewSet
from apps.locations.views import AddressViewSet
from apps.messageClini.views import MessageCliniViewSet
from apps.patientConsultation.views import PatientConsultationViewSet
from apps.profiles.views import ProfileViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()

# Rota de cadastro de Usuarios
router.register(r'Profiles', ProfileViewSet, basename='profile')
router.register(r'Address', AddressViewSet, basename='address')
router.register(r'Appointments', AppointmentViewSet, basename='appointments')
router.register(r'TimeSchedules', TimeSchedulesViewSet, basename='timeSchedules')
router.register(r'MessageClinis', MessageCliniViewSet, basename='messageClini')
router.register(r'PatientConsultations', PatientConsultationViewSet, basename='patientConsultations')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Rota para obter o token de acesso
    path("api/token-refresh/", TokenRefreshView.as_view(), name='token_refresh'),  # Rota para refresh token
    path("api/", include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
