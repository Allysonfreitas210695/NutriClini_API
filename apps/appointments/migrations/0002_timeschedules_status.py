# Generated by Django 4.2.3 on 2024-04-10 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeschedules',
            name='status',
            field=models.CharField(choices=[('unavailable', 'Unavailable'), ('available', 'Available')], default='pending', max_length=15),
        ),
    ]
