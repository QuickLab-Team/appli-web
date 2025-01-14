# Generated by Django 5.1.2 on 2025-01-14 22:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0002_produit_type_alter_produit_quantite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockage',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='stockages', to='produits.service'),
        ),
    ]
