from django.test import TestCase
from produits.models import *
from reservations.models import *

class ProduitModelTest(TestCase):

    def setUp(self):
        service1 = Service.objects.create(nom='Service 1')
        self.produit = Produit.objects.create(
            nom="Produit 1",
            quantite=10,
            stockage=Stockage.objects.create(nom='Stockage 1', service=service1)
        )
        famille1 = Famille.objects.create(nom='Famille 1')
        self.produit.familles.set([famille1])

    def test_produit_creation(self):
        """
        Test si un produit est bien créée
        """
        self.assertEqual(self.produit.nom, "Produit 1")
        self.assertEqual(self.produit.quantite, 10)
        self.assertEqual(self.produit.familles.first().nom, "Famille 1")
        self.assertEqual(self.produit.stockage.nom, "Stockage 1")
        self.assertEqual(self.produit.stockage.service.nom, "Service 1")