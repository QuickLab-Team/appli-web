from django.test import TestCase
from paniers.models import Panier, PanierProduit
from produits.models import Produit, Famille, Stockage, Service
from utilisateurs.models import Utilisateur
import datetime

class PanierProduitModelTest(TestCase):

    def setUp(self):
        self.date = datetime.date.today()

        self.utilisateur = Utilisateur.objects.create(
            nom='Nom',
            prenom='Prenom',
            email='nom.prenom@gmail.com',
        )
        self.utilisateur.set_password('password')
        self.utilisateur.save()

        self.panier = Panier.objects.create(
            date=self.date,
            utilisateur=self.utilisateur,
        )

        service1 = Service.objects.create(nom='Service 1')
        famille1 = Famille.objects.create(nom='Famille 1')
        stockage1 = Stockage.objects.create(nom='Stockage 1', service=service1)

        produit = Produit.objects.create(
            nom='Produit',
            quantite=10,
            stockage=stockage1,
            type='unite'
        )

        produit.familles.set([famille1])

        self.panier_produit = PanierProduit.objects.create(
            panier=self.panier,
            produit=produit,
            quantite=1.5,
        )

    def test_panier_produit_creation(self):
        self.assertEqual(PanierProduit.objects.count(), 1)
        self.assertEqual(self.panier.produits.count(), 1)
        self.assertEqual(self.panier_produit.produit.nom, 'Produit')
        self.assertEqual(self.panier_produit.quantite, 1.5)

    def test_update_panier(self):
        self.panier_produit.quantite = 2
        self.assertEqual(self.panier_produit.quantite, 2)

    def test_delete_panier(self):
        self.panier_produit.delete()
        self.assertEqual(PanierProduit.objects.count(), 0)
        self.assertEqual(self.panier.produits.count(), 0)