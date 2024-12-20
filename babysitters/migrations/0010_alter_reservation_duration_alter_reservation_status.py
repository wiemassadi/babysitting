# Generated by Django 5.1.3 on 2024-12-19 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('babysitters', '0009_alter_reservation_duration_alter_reservation_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='duration',
            field=models.PositiveIntegerField(help_text='Duration in minutes'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='status',
            field=models.CharField(choices=[('pending', 'En attente'), ('confirmed', 'Confirmée'), ('cancelled', 'Annulée')], default='pending', max_length=20),
        ),
    ]