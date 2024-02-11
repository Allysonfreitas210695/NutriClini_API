from django.contrib.auth.models import User
from django.db import models
from django.core.validators import EmailValidator, MinLengthValidator

# Create your models here.
class Profile(models.Model):
    TYPE_CHOICES = [
        ('nutritionist', 'Nutritionist'),
        ('patient', 'Patient'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    fullName = models.CharField(max_length=120, null=False, blank=False)
    cpf = models.CharField(max_length=14, unique=True, validators=[MinLengthValidator(limit_value=11, message="Informe um CPF válido.")], blank=False, null=False)
    email = models.EmailField(unique=True, validators=[EmailValidator("Informe um endereço de e-mail válido.")], blank=False, null=False)
    phone = models.CharField(max_length=15, blank=False, null=False) 
    specialty = models.CharField(max_length=50, blank=True, null=True) 
    crn = models.CharField(max_length=20, blank=True, null=True) 
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='patient')
    password = models.CharField(max_length=30, validators=[MinLengthValidator(limit_value=6, message="A senha deve ter pelo menos 6 caracteres.")], null=False, blank=False)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.nome