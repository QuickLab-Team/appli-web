from django.test import TestCase
from produits.models import Fournisseur

class FournisseurModelTest(TestCase):

    def setUp(self):
        self.fournisseur = Fournisseur.objects.create(nom='Fournisseur 1')

    def test_fournisseur_creation(self):
        self.assertEqual(self.fournisseur.nom, "Fournisseur 1")

    def test_fournisseur_suppression(self):
        self.fournisseur.delete()
        self.assertEqual(Fournisseur.objects.count(), 0)

    def test_fournisseur_modification(self):
        self.fournisseur.nom = "Fournisseur 2"
        self.fournisseur.save()
        self.assertEqual(self.fournisseur.nom, "Fournisseur 2")