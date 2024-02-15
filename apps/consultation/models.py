from django.contrib.auth.models import User
from django.db import models
from apps.locations.models import Address

class Consultation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consultation_as_doctor', null=True)
    user_patient = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consultation_as_patient', null=False)
    address_consulta = models.OneToOneField(Address, on_delete=models.CASCADE, related_name='consultation', null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False, blank=False, default="pending")
    date_Consulta = models.DateField(null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = "Consultation"
        verbose_name_plural = "Consultations"

    def __str__(self):
        return f"Consulta de {self.user_patient.username} em {self.date_Consulta}"

    def save(self, *args, **kwargs):
        if self.status == 'completed' and self.pk is not None:
            ConsultationHistory.objects.create(user_patient=self.user_patient, consultation=self, message='Consulta concluída')
        super().save(*args, **kwargs)

class ConsultationHistory(models.Model):
    user_patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultation_history')
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='consultation_history')
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = "ConsultationHistory"
        verbose_name_plural = "ConsultationHistories"

    def __str__(self):
        return f"Histórico de consultas para {self.user_patient.username}"
