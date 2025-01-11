from django.test import TestCase
from reservations.models import *
from produits.models import *
import datetime

class ReservationModelTest(TestCase):

    def setUp(self):
        service = Service.objects.create(nom='Service')
        produit = Produit.objects.create(
            nom="Produit",
            quantite=10,
            description="Description",
            famille=Famille.objects.create(nom='Famille'),
            stockage=Stockage.objects.create(nom='Stockage', service=service)
        )
        self.reservation = Reservation.objects.create(
            utilisateur=Utilisateur.objects.create(nom='Utilisateur'),
        )
        ReservationProduit.objects.create(
            reservation=self.reservation,
            produit=produit,
            quantite=5
        )
        ReservationProduit.objects.create(
            reservation=self.reservation,
            produit=produit,
            quantite=5
        )

    def test_reservation_creation(self):
        """
        Test si une reservation est bien créée
        """
        self.assertEqual(self.reservation.utilisateur.nom, "Utilisateur")
        self.assertEqual(self.reservation.date, datetime.date.today())
        for produit in self.reservation.produits.all():
            self.assertEqual(produit.produit.nom, "Produit")
            self.assertEqual(produit.quantite, 5)