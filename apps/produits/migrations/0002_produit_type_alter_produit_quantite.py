# Generated by Django 5.1.3 on 2024-12-10 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produit',
            name='type',
            field=models.CharField(choices=[('liquide', 'Liquide'), ('solide', 'Solide'), ('unite', 'Unité')], default='unite', max_length=10),
        ),
        migrations.AlterField(
            model_name='produit',
            name='quantite',
            field=models.FloatField(),
        ),
    ]
