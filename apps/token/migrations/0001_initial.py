# Generated by Django 4.2.3 on 2024-04-08 22:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nutritionist', '0001_initial'),
        ('patient', '0006_alter_food_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodigoReset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('nutritionist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='codigo_as_nutritionist', to='nutritionist.nutritionist')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='codigoReset_as_patient', to='patient.patient')),
            ],
            options={
                'verbose_name': 'CodigoReset',
                'verbose_name_plural': 'CodigoResets',
            },
        ),
    ]
