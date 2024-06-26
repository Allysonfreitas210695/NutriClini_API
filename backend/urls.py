from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.nutritionist.views import NutritionistViewSet
from apps.patient.views import AvaliationViewSet, FoodViewSet, MealPlanViewSet, MealViewSet, PatientViewSet, PrescriptionViewSet
from apps.token.views import CustomTokenObtainPairView, CustomTokenRefreshView, EnviarCodigoSenhaAPIView, ResetPasswordAPIView, VerificarCodigoView
from apps.appointments.views import AppointmentViewSet, TimeSchedulesViewSet
from apps.locations.views import AddressViewSet
from apps.messageClini.views import MessageCliniViewSet
from apps.consultation.views import ConsultationViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


router = DefaultRouter()


# Rota de cadastro de Usuarios
router.register(r'Address', AddressViewSet, basename='address')

router.register(r'Appointments', AppointmentViewSet, basename='appointments')

router.register(r'Avaliation', AvaliationViewSet, basename='avaliations')

router.register(r'food', FoodViewSet, basename='foods')

router.register(r'Consultations', ConsultationViewSet, basename='consultations')

router.register(r'Nutritionist', NutritionistViewSet, basename='nutritionists')

router.register(r'Patient', PatientViewSet, basename='patients')

router.register(r'Prescription', PrescriptionViewSet, basename='prescriptions')

router.register(r'TimeSchedule', TimeSchedulesViewSet, basename='timeSchedules')

router.register(r'mealPlan', MealPlanViewSet, basename='mealPlans')

router.register(r'meal', MealViewSet, basename='meals')

router.register(r'MessageClinis', MessageCliniViewSet, basename='messageClini')


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token/", CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Rota para obter o token de acesso
    path("api/token-refresh/", CustomTokenRefreshView.as_view(), name='token_refresh'),  # Rota para refresh token
    path("api/enviar_codigo/", EnviarCodigoSenhaAPIView.as_view(), name='enviar_codigo'),  # Rota para enviar código de verificação por e-mail
    path("api/verificacao_codigo/", VerificarCodigoView.as_view(), name='enviar_codigo'),
    path('api/reset-password/', ResetPasswordAPIView.as_view(), name='reset_password'),
    path("api/", include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
