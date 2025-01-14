# Generated by Django 5.1.4 on 2025-01-14 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0010_alter_reservation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='etat',
            field=models.CharField(choices=[('attente', 'En attente'), ('valide', 'Validé'), ('refuse', 'Refusé'), ('pre_reservation_attente', 'Pré-réservation en attente'), ('pre_reservation_refuse', 'Pré-réservation refusé'), ('attente_recuperation', 'En attente de récupération'), ('termine', 'Terminé')], default='attente', max_length=50),
        ),
    ]
