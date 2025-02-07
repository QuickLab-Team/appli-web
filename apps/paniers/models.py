from django.db import models
from utilisateurs.models import Utilisateur
from produits.models import Produit
from produits.models import conversion_liquides, conversion_solides

# Create your models here.

class Panier(models.Model):
    """
    Panier
    """
    id = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return "{0}".format(self.utilisateur)
    
class PanierProduit(models.Model):
    """
    PanierProduit
    """
    id = models.AutoField(primary_key=True)
    panier = models.ForeignKey(Panier, related_name='produits', on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.FloatField()
    
    def __str__(self):
        return "{0} - {1} - {2}".format(self.panier, self.produit, self.quantite)
    
    def add_quantite(self, quantite, unite = None):
        if self.produit.type == 'liquide':
            if unite is None:
                unite = list(conversion_liquides.keys())[0]

            if unite in conversion_liquides:
                self.quantite += quantite * conversion_liquides[unite]
            else:
                raise ValueError(f"Unité invalide pour un liquide : {unite}")
        elif self.produit.type == 'solide':
            if unite is None:
                unite = list(conversion_solides.keys())[0]
                
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