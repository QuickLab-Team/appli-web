# Generated by Django 5.1.4 on 2025-01-07 15:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0005_fournisseur_alter_produit_fournisseur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='fournisseur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='produits.fournisseur'),
        ),
    ]
