from django.db import models
from utilisateurs.models import Utilisateur
from produits.models import Produit, conversion_liquides, conversion_solides

# Create your models here.

class MessageReservation(models.Model):
    """
    MessageReservation
    """
    id = models.AutoField(primary_key=True)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    reservation = models.ForeignKey('Reservation', related_name='messages', on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    
    def __str__(self):
        return "{0}".format(self.message)

class Reservation(models.Model):
    """
    Reservation
    """
    id = models.AutoField(primary_key=True)
    titre = models.CharField(max_length=255, default='Réservation')
    ETAT_CHOICES = [
        ('attente', 'En attente'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),

        ('pre_reservation_attente', 'Pré-réservation en attente'),
        ('pre_reservation_refuse', 'Pré-réservation refusé'),

        ('attente_recuperation', 'En attente de récupération'),
        ('termine', 'Terminé'),
    ]
    etat = models.CharField(
        max_length=50,
        choices=ETAT_CHOICES,
        default='attente',
    )
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{0}".format(self.utilisateur)
    
    def get_etats(self):
        return self.ETAT_CHOICES

class ReservationProduit(models.Model):
    """
    ReservationProduit
    """
    id = models.AutoField(primary_key=True)
    reservation = models.ForeignKey(Reservation, related_name='produits', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.FloatField()
    
    def __str__(self):
        return "{0} - {1} - {2}".format(self.reservation, self.produit, self.quantite)
    
    def add_quantite(self, quantite, unite):
        if self.produit.type == 'liquide':
            if unite in conversion_liquides:
                self.quantite += quantite * conversion_liquides[unite]
            else:
                raise ValueError(f"Unité invalide pour un liquide : {unite}")
        elif self.produit.type == 'solide':
            if unite in conversion_solides:
                self.quantite += quantite * conversion_solides[unite]
            else:
                raise ValueError(f"Unité invalide pour un solide : {unite}")
        else:
            self.quantite += quantite
            
        self.save()

    def get_quantite(self):
        if self.produit.type == 'liquide':
            conversion = dict(sorted(conversion_liquides.items(), key=lambda item:[1]))
        elif self.produit.type == 'solide':
            conversion = dict(sorted(conversion_solides.items(), key=lambda item:[1]))
        else:
            return self.quantite

        for unite, valeur in conversion.items():
            if self.quantite >= valeur:
                return self.quantite / valeur
            
        return None
    
    def get_unite(self):
        if self.produit.type == 'liquide':
            conversion = dict(sorted(conversion_liquides.items(), key=lambda item:[1]))
        elif self.produit.type == 'solide':
            conversion = dict(sorted(conversion_solides.items(), key=lambda item:[1]))
        else:
            return 'unite'

        for unite, valeur in conversion.items():
            if self.quantite >= valeur:
                return unite
            
        return None