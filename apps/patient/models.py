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
    password = models.CharField(max_length=30, validators=[MinLengthValidator(limit_value=6, message="Password must be at least 6 characters.")], null=True, blank=True)
    observation = models.TextField(blank=True, null=True) 

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return self.fullName
    
    def save(self, *args, **kwargs):
        if not self.pk:
            send_mail(
                'Cadastro de Paciente',
                '',
                'nutriclinicn@gmail.com',
                [self.email],
                html_message=f"""
                    <html>
                    <head>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                            }}
                            .container {{
                                max-width: 600px;
                                margin: 0 auto;
                                padding: 20px;
                                border: 1px solid #ccc;
                                border-radius: 5px;
                            }}
                            h3 {{
                                color: #333;
                            }}
                            p {{
                                margin-bottom: 10px;
                            }}
                            a {{
                                color: #007bff;
                                text-decoration: none;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h3>Bem-vindo à NutriClinic, {self.fullName}!</h3>
                            <p>Obrigado por se cadastrar em nossa clínica.</p>
                            <p>Aqui estão os detalhes do seu cadastro:</p>
                            <ul>
                                <li><strong>Login:</strong> {self.email}</li>
                                <li><strong>Senha:</strong> {self.password}</li>
                            </ul>
                            <p>Para redefinir sua senha, acesse o seguinte link:</p>
                            <p><a href="https://nutri-clinic-frontend.vercel.app/forgotPassword">Redefinir Senha</a></p>
                        </div>
                    </body>
                    </html>
                """,
                fail_silently=False
            )
        super().save(*args, **kwargs)

class MealPlan(models.Model):
    name = models.CharField(max_length=255)
    descricao = models.TextField()
    observation = models.TextField(blank=True, null=True)
    daysOfWeek = models.CharField(max_length=255)
    status = models.CharField(max_length=10)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = "MealPlan"
        verbose_name_plural = "MealPlans"

    def __str__(self):
        return self.name

class Meal(models.Model):
    name = models.CharField(max_length=255)
    time = models.TimeField(blank=False, null=False, verbose_name='Time Value')
    observation = models.TextField(blank=True, null=True)
    mealPlan = models.ForeignKey(MealPlan, on_delete=models.CASCADE, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')

    class Meta:
        verbose_name = "Meal"
        verbose_name_plural = "Meals"

    def __str__(self):
        return self.name

class Food(models.Model):
    name = models.CharField(max_length=255)
    measure = models.CharField(max_length=255)
    quantity = models.IntegerField(blank=False, null=False)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, blank=False, null=False)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    class Meta:
        verbose_name = "Food"
        verbose_name_plural = "Foods"

    def __str__(self):
        return self.name

class Avaliation(models.Model):
    type = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=False, null=False)
    height = models.FloatField(blank=False, null=False)
    current_weight = models.FloatField(blank=False, null=False)
    ideal_weight = models.FloatField(blank=False, null=False)
    observation = models.TextField(blank=False, null=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Avaliation"
        verbose_name_plural = "Avaliations"

    def __str__(self):
        return self.description

class Prescription(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    date = models.DateField(blank=False, null=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Prescription"
        verbose_name_plural = "Prescriptions"

    def __str__(self):
        return self.name
