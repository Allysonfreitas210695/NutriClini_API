from django.contrib.auth.models import User
from apps.locations.models import Address
from django.db import models

from apps.nutritionist.models import Nutritionist

class TimeSchedules(models.Model):
    STATUS_CHOICES = [
        ('unavailable', 'Unavailable'),
        ('available', 'Available'),
    ]

    time_value = models.TimeField(verbose_name='Time Value')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, null=False, blank=False, default="available")
    class Meta:
        verbose_name = "TimeSchedule"
        verbose_name_plural = "TimeSchedules"

    def __str__(self):
        return str(self.time_value)

class Appointment(models.Model):
    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE, related_name='appointment_nutritionist', null=False, blank=False)
    date_appointments = models.DateField(null=False)
    service_location = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='appointments', null=False)
    schedules = models.ManyToManyField(TimeSchedules, related_name='appointments', verbose_name='TimeSchedules', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return f"{self.user} - {self.date_appointments}"
