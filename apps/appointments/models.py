from django.contrib.auth.models import User
from apps.locations.models import Address
from django.db import models

class TimeSchedules(models.Model):
    time_value = models.TimeField(verbose_name='Time Value')

    class Meta:
        verbose_name = "TimeSchedule"
        verbose_name_plural = "TimeSchedules"

    def __str__(self):
        return str(self.time_value)

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', null=True)
    date_appointments = models.DateField(null=False)
    service_location = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='appointments', null=False)
    schedules = models.ManyToManyField(TimeSchedules, related_name='appointments', verbose_name='Schedules', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return f"{self.user} - {self.date_appointments}"
