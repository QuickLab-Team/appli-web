from django.test import TestCase
from django.urls import reverse
from utilisateurs.models import Utilisateur
from produits.models import Produit, Stockage, Service

class PanierTestViews(TestCase):

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

    def test_url_panier(self):
        response = self.client.get(reverse('paniers:panier'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paniers/etudiants/panier.html')

    def test_url_ajouter_produit_panier(self):
        response = self.client.post(reverse('paniers:ajouter_produit_panier'), {
            'quantite': 1,
            'unite': 'kg',
            'produit_id': self.produit.id
        })
        self.assertEqual(response.status_code, 302)

        response = self.client.post(reverse('paniers:ajouter_produit_panier'), {
            'unite': 'kg',
            'produit_id': self.produit.id
        })
        self.assertEqual(response.status_code, 400)

        response = self.client.post(reverse('paniers:ajouter_produit_panier'), {
            'quantite': 1,
            'produit_id': self.produit.id
        })
        self.assertEqual(response.status_code, 400)

    def test_url_supprimer_produit_panier(self):
        # produit non existant
        response = self.client.post(reverse('paniers:supprimer_produit_panier'), {
            'produit_id': self.produit.id + 1
        })
        self.assertEqual(response.status_code, 404)
    
        response = self.client.post(reverse('paniers:supprimer_produit_panier'), {
            'produit_id': self.produit.id
        })
        self.assertEqual(response.status_code, 302)

        # aucun produit dans la requête
        response = self.client.post(reverse('paniers:supprimer_produit_panier'), {
        })
        self.assertEqual(response.status_code, 404)

    def test_url_reserver_panier(self):
        self.client.post(reverse('paniers:ajouter_produit_panier'), {
            'quantite': 1,
            'unite': 'kg',
            'produit_id': self.produit.id
        })
        response = self.client.post(reverse('paniers:reserver_panier'))
        self.assertEqual(response.status_code, 302)

        # panier vide
        response = self.client.post(reverse('paniers:reserver_panier'))
        self.assertEqual(response.status_code, 400)