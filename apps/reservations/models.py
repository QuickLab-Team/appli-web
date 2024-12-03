from django.db import models
from utilisateurs.models import Utilisateur
from produits.models import Produit

# Create your models here.

class Reservation(models.Model):
    """
    Reservation
    """
    id = models.AutoField(primary_key=True)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return "{0}".format(self.utilisateur)

class ReservationProduit(models.Model):
    """
    ReservationProduit
    """
    id = models.AutoField(primary_key=True)
    reservation = models.ForeignKey(Reservation, related_name='produits', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    
    def __str__(self):
        return "{0} - {1} - {2}".format(self.reservation, self.produit, self.quantite)