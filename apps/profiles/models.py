from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, EmailValidator
from django.core.exceptions import ValidationError

class Profile(models.Model):
    TYPE_CHOICES = [
        ('nutritionist', 'Nutritionist'),
        ('patient', 'Patient'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', null=True)
    fullName = models.CharField(max_length=120, null=False, blank=False)
    cpf = models.CharField(max_length=14, unique=True, validators=[MinLengthValidator(limit_value=11, message="Enter a valid CPF.")], blank=False, null=False)
    email = models.EmailField(unique=True, validators=[EmailValidator("Enter a valid email address.")], blank=False, null=False)
    phone = models.CharField(max_length=15, blank=False, null=False) 
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False, blank=False, default="active")
    dateOfBirth = models.DateField(null=True, blank=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True, null=True)
    number = models.CharField(max_length=10, blank=True, null=True)
    neighborhood = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    specialty = models.CharField(max_length=50, blank=True, null=True) 
    crn = models.CharField(max_length=20, blank=True, null=True) 
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='patient')
    password = models.CharField(max_length=30, validators=[MinLengthValidator(limit_value=6, message="Password must be at least 6 characters.")], null=False, blank=False)
    observation = models.TextField(blank=True, null=True) 

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.fullName
    
    def save(self, *args, **kwargs):
        if self.type == 'patient':
            required_fields = ['gender', 'dateOfBirth', 'cep', 'street', 'number', 'neighborhood', 'city', 'state', 'observation']
            missing_fields = [field.capitalize() for field in required_fields if not getattr(self, field)]
            
            if missing_fields:
                raise ValidationError(f"The following fields are required for patient profiles: {', '.join(missing_fields)}")

        super().save(*args, **kwargs)
