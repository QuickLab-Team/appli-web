# Generated by Django 5.1.4 on 2024-12-10 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='titre',
            field=models.CharField(default='Réservation', max_length=255),
        ),
    ]
