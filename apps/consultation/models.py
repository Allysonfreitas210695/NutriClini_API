from django.contrib.auth.models import User
from django.db import models
from apps.locations.models import Address
from apps.nutritionist.models import Nutritionist
from apps.patient.models import Patient

class Consultation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('finished', 'Finished'),
    ]

    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE, related_name='consultation_nutritionist', null=False, blank=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='consultation_as_patient', null=False)
    address_consulta = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='consultation', null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False, blank=False, default="pending")
    date_Consulta = models.DateTimeField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"

    def __str__(self):
        return f"Consulta de {self.patient.username} em {self.date_Consulta}"


