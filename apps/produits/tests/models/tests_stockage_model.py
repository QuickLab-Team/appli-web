from django.test import TestCase
from produits.models import *
from reservations.models import *

class StockageModelTest(TestCase):

    def setUp(self):
        self.stockage = Stockage.objects.create(nom='Stockage 1', service=Service.objects.create(nom='Service 1'))

    def test_stockage_creation(self):
        self.assertEqual(self.stockage.nom, "Stockage 1")
        self.assertEqual(self.stockage.service.nom, "Service 1")

    def test_stockage_suppression(self):
        self.stockage.delete()
        self.assertEqual(Stockage.objects.count(), 0)

    def test_stockage_modification(self):
        self.stockage.nom = "Stockage 2"
        self.stockage.save()
        self.assertEqual(self.stockage.nom, "Stockage 2")