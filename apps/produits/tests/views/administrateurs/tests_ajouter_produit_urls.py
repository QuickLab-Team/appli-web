from django.test import TestCase
from django.urls import reverse
from utilisateurs.models import Utilisateur
from produits.models import Produit, Stockage, Service

class AdminAjouterProduitTestViews(TestCase):

    def setUp(self):
        utilisateur = Utilisateur.objects.create(
            nom='Utilisateur',
            prenom='Prenom',
            email='utilisateur@gmail.com',
            role='administrateur'
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

    def test_url_ajouter_produit(self):
        response = self.client.get(reverse('produits:ajouter_produit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'produits/preparateurs/ajouter_produit.html')
