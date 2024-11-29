from django.test import TestCase
from reservation_models.models import *

class ProduitModelTest(TestCase):

    def setUp(self):
        service1 = Service.objects.create(nom='Service 1')
        self.produit = Produit.objects.create(
            nom="Produit 1",
            quantite=10,
            description="Description1",
            famille=Famille.objects.create(nom='Famille 1'),
            stockage=Stockage.objects.create(nom='Stockage 1', service=service1)
        )


    def test_produit_creation(self):
        """
        Test si un produit est bien créée
        """
        self.assertEqual(self.produit.nom, "Produit 1")
        self.assertEqual(self.produit.quantite, 10)
        self.assertEqual(self.produit.description, "Description1")
        self.assertEqual(self.produit.famille.nom, "Famille 1")
        self.assertEqual(self.produit.stockage.nom, "Stockage 1")
        self.assertEqual(self.produit.stockage.service.nom, "Service 1")