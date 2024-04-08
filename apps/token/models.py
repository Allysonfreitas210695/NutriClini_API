from django.db import models

from apps.nutritionist.models import Nutritionist
from apps.patient.models import Patient

class CodigoReset(models.Model):
    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE, related_name='codigo_as_nutritionist', null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='codigoReset_as_patient', null=True)
    codigo = models.CharField(max_length=15, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = "CodigoReset"
        verbose_name_plural = "CodigoResets"

    def __str__(self):
        return self.codigo
