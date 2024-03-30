# Generated by Django 4.2.3 on 2024-03-30 18:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nutritionist', '0001_initial'),
        ('patient', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='nutritionist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patients', to='nutritionist.nutritionist'),
        ),
    ]