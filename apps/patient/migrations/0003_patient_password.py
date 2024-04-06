# Generated by Django 4.2.3 on 2024-04-06 09:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_alter_patient_nutritionist'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='password',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[django.core.validators.MinLengthValidator(limit_value=6, message='Password must be at least 6 characters.')]),
        ),
    ]
