from django.core.management.base import BaseCommand
from reservation_models.models import *
import random

class Command(BaseCommand):
    help = 'Ajoute des données en BD'

    def handle(self, *args, **options):

        self.stdout.write('Suppression des données...')

        Famille.objects.all().delete()
        Service.objects.all().delete()
        Stockage.objects.all().delete()
        Produit.objects.all().delete()

        self.stdout.write('Création des données...')

        # Familles
        famille1 = Famille.objects.create(nom='Famille 1')
        famille2 = Famille.objects.create(nom='Famille 2')
        famille3 = Famille.objects.create(nom='Famille 3')

        # Services
        service1 = Service.objects.create(nom='Service 1')
        service2 = Service.objects.create(nom='Service 2')
        service3 = Service.objects.create(nom='Service 3')

        # Stockage 
        stockage1 = Stockage.objects.create(nom='Stockage 1', service=service1)
        stockage2 = Stockage.objects.create(nom='Stockage 2', service=service2)

        # Produits
        for i in range(1, 5):
            produit = Produit.objects.create(
                nom='Produit {0}'.format(i),
                quantite=random.randint(1, 1000),
                description='Description produit {0}'.format(i),
                famille=famille1,
                stockage=stockage1
            )
        
        for i in range(5, 10):
            produit = Produit.objects.create(
                nom='Produit {0}'.format(i),
                quantite=random.randint(1, 1000),
                description='Description produit {0}'.format(i),
                famille=famille2,
                stockage=stockage2
            )

        for i in range(10, 15):
            produit = Produit.objects.create(
                nom='Produit {0}'.format(i),
                quantite=random.randint(1, 1000),
                description='Description produit {0}'.format(i),
                famille=famille1,
                stockage=stockage2
            )

        self.stdout.write('Données créées avec succès !')