# Generated by Django 5.1.3 on 2024-11-29 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReservationProduit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantite', models.IntegerField()),
            ],
        ),
    ]
