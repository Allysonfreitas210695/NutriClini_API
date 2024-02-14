# Generated by Django 4.2.3 on 2024-02-14 22:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullName', models.CharField(max_length=120)),
                ('cpf', models.CharField(max_length=14, unique=True, validators=[django.core.validators.MinLengthValidator(limit_value=11, message='Enter a valid CPF.')])),
                ('email', models.EmailField(max_length=254, unique=True, validators=[django.core.validators.EmailValidator('Enter a valid email address.')])),
                ('phone', models.CharField(max_length=15)),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10, null=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('inactive', 'Inactive')], default='active', max_length=10)),
                ('dateOfBirth', models.DateField(blank=True, null=True)),
                ('cep', models.CharField(blank=True, max_length=10, null=True)),
                ('street', models.CharField(blank=True, max_length=255, null=True)),
                ('number', models.CharField(blank=True, max_length=10, null=True)),
                ('neighborhood', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('specialty', models.CharField(blank=True, max_length=50, null=True)),
                ('crn', models.CharField(blank=True, max_length=20, null=True)),
                ('type', models.CharField(choices=[('nutritionist', 'Nutritionist'), ('patient', 'Patient')], default='patient', max_length=20)),
                ('password', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(limit_value=6, message='Password must be at least 6 characters.')])),
                ('observation', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
