from django.contrib.auth.models import User
from django.db import models
from apps.nutritionist.models import Nutritionist

class Address(models.Model):
    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE, related_name='address_nutritionist', null=False, blank=False)
    full_name = models.CharField(max_length=255, verbose_name='Nome completo', blank=False, null=False)
    cep = models.CharField(max_length=10, verbose_name='CEP', blank=False, null=False)
    street = models.CharField(max_length=255, verbose_name='Rua', blank=False, null=False)
    number = models.CharField(max_length=10, verbose_name='Número', blank=False, null=False)
    neighborhood = models.CharField(max_length=255, verbose_name='Bairro', blank=False, null=False)
    city = models.CharField(max_length=255, verbose_name='Cidade', blank=False, null=False)
    state = models.CharField(max_length=255, verbose_name='Estado', blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Address"

    def __str__(self):
        return self.full_name
