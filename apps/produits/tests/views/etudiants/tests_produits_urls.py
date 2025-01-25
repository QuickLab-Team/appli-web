from django.test import TestCase
from django.urls import reverse
from utilisateurs.models import Utilisateur
from produits.models import Produit, Stockage, Service

class EtudiantsProduitsTestViews(TestCase):

    def setUp(self):
        utilisateur = Utilisateur.objects.create(
            nom='Utilisateur',
            prenom='Prenom',
            email='utilisateur@gmail.com',
        )
        utilisateur.set_password('password')
        utilisateur.save()

        produit = Produit.objects.create(
            nom='Produit 1',
            quantite=1000,
            stockage=Stockage.objects.create(
                nom='Stockage 1', 
                service=Service.objects.create(nom='Service 1')
            ),
            type='solide'
        )
        produit.save()

        self.produit =  produit
        self.client.login(username='utilisateur@gmail.com', password='password')

    def test_url_produits(self):
        response = self.client.get(reverse('produits:produits'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produits/etudiants/produits.html')

    def test_url_produit(self):
        response = self.client.get(reverse('produits:produit', kwargs={'produit_id': self.produit.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produits/etudiants/produit.html')

    def test_url_importer_produits(self):
        response = self.client.get(reverse('produits:importer_produits'))
        self.assertEqual(response.status_code, 403)

    def test_url_ajouter_produit(self):
        response = self.client.post(reverse('produits:ajouter_produit'))
        self.assertEqual(response.status_code, 403)

    def test_url_modifier_produit(self):
        response = self.client.post(reverse('produits:modifier_produit', kwargs={'produit_id': self.produit.id}))
        self.assertEqual(response.status_code, 403)

    def test_url_supprimer_produit(self):
        response = self.client.post(reverse('produits:supprimer_produit', kwargs={'produit_id': self.produit.id}))
        self.assertEqual(response.status_code, 403)