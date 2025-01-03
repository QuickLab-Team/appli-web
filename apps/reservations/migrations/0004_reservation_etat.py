# Generated by Django 5.1.4 on 2024-12-10 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_reservation_titre'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='etat',
            field=models.CharField(choices=[('pret', 'Prêt'), ('en_cours', 'En cours'), ('termine', 'Terminé'), ('en_attente', 'En attente')], default='en_attente', max_length=20),
        ),
    ]
