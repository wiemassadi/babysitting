# Generated by Django 5.1.3 on 2024-12-20 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babysitters', '0010_alter_reservation_duration_alter_reservation_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', 'En attente'), ('confirmed', 'Confirmée'), ('cancelled', 'Annulée'), ('passed', 'Terminée')], default='pending', max_length=20),
        ),
    ]
