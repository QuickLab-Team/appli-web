from django.test import TestCase
from produits.models import *
from reservations.models import *

class FamilleModelTest(TestCase):

    def setUp(self):
        self.famille = Famille.objects.create(nom='Famille 1')

    def test_famille_creation(self):
        self.assertEqual(self.famille.nom, "Famille 1")

    def test_famille_suppression(self):
        self.famille.delete()
        self.assertEqual(Famille.objects.count(), 0)

    def test_famille_modification(self):
        self.famille.nom = "Famille 2"
        self.famille.save()
        self.assertEqual(self.famille.nom, "Famille 2")