# Generated by Django 5.1.4 on 2025-01-14 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0008_remove_produit_famille_produit_date_ajout_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='description',
        ),
    ]
