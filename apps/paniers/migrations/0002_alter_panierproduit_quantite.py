# Generated by Django 5.1.4 on 2025-01-10 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paniers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='panierproduit',
            name='quantite',
            field=models.FloatField(),
        ),
    ]
