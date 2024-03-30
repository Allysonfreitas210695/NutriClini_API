from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from apps.nutritionist.models import Nutritionist
from django.core.mail import send_mail
from decouple import config
    
class Patient(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE, related_name='patients', null=False, blank=False)
    fullName = models.CharField(max_length=120, null=False, blank=False)
    cpf = models.CharField(max_length=14, unique=True, validators=[MinLengthValidator(limit_value=11, message="Enter a valid CPF.")], blank=False, null=False)
    email = models.EmailField(unique=True, validators=[EmailValidator("Enter a valid email address.")], blank=False, null=False)
    phone = models.CharField(max_length=15, blank=False, null=False) 
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False, blank=False, default="active")
    dateOfBirth = models.DateField(null=False, blank=False)
    cep = models.CharField(max_length=10, blank=False, null=False)
    street = models.CharField(max_length=255, blank=False, null=False)
    number = models.CharField(max_length=10, blank=False, null=False)
    neighborhood = models.CharField(max_length=255, blank=False, null=False)
    city = models.CharField(max_length=255, blank=False, null=False)
    state = models.CharField(max_length=255, blank=False, null=False)
    observation = models.TextField(blank=True, null=True) 


    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return self.fullName
    
    def save(self, *args, **kwargs):
        if not self.pk:
            print("you teste")
            print(config("EMAIL_HOST_USER"))
            send_mail(
                'Cadastro de Paciente',
                '', 
                config("EMAIL_HOST_USER"), 
                [self.email], 
                html_message=f"""
                                <html>
                                <head></head>
                                <body>
                                    <h3>Bem-vindo à NutriClinic, {self.fullName}!</h3>
                                    <p>Obrigado por se cadastrar em nossa clínica.</p>
                                </body>
                                </html>
                                """,
                fail_silently=False
            )
            print("passou")
        super().save(*args, **kwargs)
