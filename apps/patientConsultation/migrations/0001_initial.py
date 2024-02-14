# Generated by Django 4.2.3 on 2024-02-14 22:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientConsultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descrition', models.CharField(max_length=255, verbose_name='Nome completo')),
                ('date_Consulta', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('adress_consulta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_consultation', to='locations.address')),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_consultation', to=settings.AUTH_USER_MODEL)),
                ('user_pacient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient_consultation_pacient', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'PatientConsultation',
                'verbose_name_plural': 'PatientConsultations',
            },
        ),
    ]
