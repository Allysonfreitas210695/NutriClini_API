# Generated by Django 4.2.3 on 2024-04-07 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('patient', '0005_alter_meal_time'),
        ('consultation', '0002_alter_consultation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='address_consulta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultation', to='locations.address'),
        ),
        migrations.AlterField(
            model_name='consultation',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultation_as_patient', to='patient.patient'),
        ),
    ]
