# Generated by Django 5.1.3 on 2024-11-29 13:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produits', '0001_initial'),
        ('reservations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='utilisateur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservationproduit',
            name='produit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.produit'),
        ),
        migrations.AddField(
            model_name='reservationproduit',
            name='reservation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='produits', to='reservations.reservation'),
        ),
    ]