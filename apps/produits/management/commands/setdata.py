from django.core.management.base import BaseCommand
from produits.models import *
from reservations.models import *
import random

class Command(BaseCommand):
    help = 'Ajoute des données en BD'

    def handle(self, *args, **options):

        self.stdout.write('Suppression des données...')

        Famille.objects.all().delete()
        Service.objects.all().delete()
        Stockage.objects.all().delete()
        Produit.objects.all().delete()
        Utilisateur.objects.all().delete()
        Reservation.objects.all().delete()
        ReservationProduit.objects.all().delete()

        self.stdout.write('Données supprimées avec succès !')

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
                id=i,
                nom='Produit {0}'.format(i),
                quantite=random.randint(1, 1000),
                description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Sint, alias vel, earum laborum cupiditate illum nostrum excepturi dignissimos eligendi deserunt consectetur iusto sunt, reiciendis ad maiores nulla in. Porro molestiae facilis tempora eius repellat sapiente tenetur fugiat, id animi explicabo quae enim aut sequi aperiam! Maiores ullam commodi quos consequatur?',
                famille=famille1,
                stockage=stockage1,
                type='liquide'
            )
        
        for i in range(5, 10):
            produit = Produit.objects.create(
                id=i,
                nom='Produit {0}'.format(i),
                quantite=random.randint(1, 1000),
                description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Sint, alias vel, earum laborum cupiditate illum nostrum excepturi dignissimos eligendi deserunt consectetur iusto sunt, reiciendis ad maiores nulla in. Porro molestiae facilis tempora eius repellat sapiente tenetur fugiat, id animi explicabo quae enim aut sequi aperiam! Maiores ullam commodi quos consequatur?',
                famille=famille2,
                stockage=stockage2,
                type='solide'
            )

        for i in range(10, 15):
            produit = Produit.objects.create(
                id=i,
                nom='Produit {0}'.format(i),
                quantite=random.randint(1, 1000),
                description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Sint, alias vel, earum laborum cupiditate illum nostrum excepturi dignissimos eligendi deserunt consectetur iusto sunt, reiciendis ad maiores nulla in. Porro molestiae facilis tempora eius repellat sapiente tenetur fugiat, id animi explicabo quae enim aut sequi aperiam! Maiores ullam commodi quos consequatur?',
                famille=famille1,
                stockage=stockage2,
                type='unite'
            )

        # Utilisateurs
        for i in range(1, 20):
            utilisateur = Utilisateur.objects.create(
                id=i,
                nom='Utilisateur {0}'.format(i),
                prenom='Prenom {0}'.format(i),
                email='nom{0}.prenom{0}@gmail.com'.format(i),
            )
            utilisateur.set_password('password{0}'.format(i))
            utilisateur.save()

        Utilisateur.objects.create_superuser(
            nom='Admin',
            prenom='Admin',
            email='admin@gmail.com',
            password='admin',
            role='administrateur'
        )


        # # Réservations
        # for i in range(1, 5):
        #     reservation = Reservation.objects.create(
        #         id=i,
        #         utilisateur=Utilisateur.objects.get(id=random.randint(1, 19)),
        #         date='2021-01-01'
        #     )

        # #Réservations Produits
        # for i in range(1, 15):
        #     reservation_produit = ReservationProduit.objects.create(
        #         reservation=Reservation.objects.get(id=random.randint(1, 4)),
        #         produit=Produit.objects.get(id=random.randint(1, 14)),
        #         quantite=random.randint(1, 10)
        #     )

        self.stdout.write('Données créées avec succès !')