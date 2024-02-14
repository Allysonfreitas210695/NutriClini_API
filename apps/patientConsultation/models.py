from django.contrib.auth.models import User
from django.db import models
from apps.locations.models import Address

class PatientConsultation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_consultation', null=True)
    user_pacient = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_consultation_pacient', null=False)
    adress_consulta = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='patient_consultation', null=False)
    date_Consulta = models.DateField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = "PatientConsultation"
        verbose_name_plural = "PatientConsultations"

    def __str__(self):
        return self.description
