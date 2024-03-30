from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, EmailValidator
from django.core.exceptions import ValidationError

class Nutritionist(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    fullName = models.CharField(max_length=120, null=False, blank=False)
    cpf = models.CharField(max_length=14, unique=True, validators=[MinLengthValidator(limit_value=11, message="Enter a valid CPF.")], blank=False, null=False)
    email = models.EmailField(unique=True, validators=[EmailValidator("Enter a valid email address.")], blank=False, null=False)
    phone = models.CharField(max_length=15, blank=False, null=False) 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False, blank=False, default="active")
    specialty = models.CharField(max_length=50, blank=False, null=False) 
    crn = models.CharField(max_length=20, blank=False, null=False) 
    password = models.CharField(max_length=30, validators=[MinLengthValidator(limit_value=6, message="Password must be at least 6 characters.")], null=False, blank=False)

    class Meta:
        verbose_name = "Nutritionist"
        verbose_name_plural = "Nutritionists"

    def __str__(self):
        return self.fullName
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
