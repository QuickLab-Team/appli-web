from django.test import TestCase
from paniers.models import Panier
from utilisateurs.models import Utilisateur
import datetime

class PanierModelTest(TestCase):

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

    def test_panier_creation(self):
        self.assertEqual(Panier.objects.count(), 1)
        self.assertEqual(self.panier.utilisateur.nom, 'Nom')
        self.assertEqual(self.panier.utilisateur.prenom, 'Prenom')
        self.assertEqual(self.panier.utilisateur.email, 'nom.prenom@gmail.com')

    def test_string_representation(self):
        self.assertEqual(str(self.panier), str(self.utilisateur))

    def test_update_panier(self):
        self.panier.id = 10
        self.assertEqual(self.panier.id, 10)

    def test_delete_panier(self):
        self.panier.delete()
        self.assertEqual(Panier.objects.count(), 0)