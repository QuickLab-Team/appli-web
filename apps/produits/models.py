from django.db import models
from django.utils import timezone


# Create your models here.

conversion_liquides = {
    'L': 1,
    'cl': 0.01,
    'ml': 0.001
}

conversion_solides = {
    'kg': 1,
    'g': 0.001,
    'mg': 0.000001
}

class Service(models.Model):
    """
    Service
    """
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return "{0} {1}".format(self.id, self.nom)
    
class Stockage(models.Model):
    """
    Stockage
    """
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='stockages')
    
    def __str__(self):
        return "{0} {1}".format(self.id, self.nom)
    
class Famille(models.Model):
    """
    Famille
    """
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return "{0} {1}".format(self.id, self.nom)

class Fournisseur(models.Model):
    """
    Fournisseur
    """
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    
    def __str__(self):
        return "{0} {1}".format(self.id, self.nom)

class Produit(models.Model):
    """
    Produit
    """ 
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    quantite = models.FloatField()
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, null=True, blank=True)
    familles = models.ManyToManyField(Famille, blank=True)
    date_ajout = models.DateTimeField(default=timezone.now)
    stockage = models.ForeignKey(Stockage, on_delete=models.CASCADE)
    seuil = models.FloatField(default=0.0)
    type = models.CharField(max_length=10, choices=[('liquide', 'Liquide'), ('solide', 'Solide'), ('unite', 'Unité')], default='unite')
    
    def __str__(self):
        return "{0} {1}".format(self.id, self.nom)
    
    def add_quantite(self, quantite, unite = None):
        if self.type == 'liquide':
            if unite is None:
                unite = 'l'

            if unite in conversion_liquides:
                self.quantite += quantite * conversion_liquides[unite]
            else:
                raise ValueError(f"Unité invalide pour un liquide : {unite}")
        elif self.type == 'solide':
            if unite is None:
                unite = 'kg'
            if unite in conversion_solides:
                self.quantite += quantite * conversion_solides[unite]
            else:
                raise ValueError(f"Unité invalide pour un solide : {unite}")
        else:
            self.quantite += quantite
            
        self.save()

    
    def add_type(self, unite):
        if 'l' in unite:
            self.type = 'liquide'
        elif 'g' in unite:
            self.type = 'solide'
        else:
            self.type = 'unite'


    def get_quantite(self):
        if self.type == 'liquide':
            conversion = dict(sorted(conversion_liquides.items(), key=lambda item:[1]))
        elif self.type == 'solide':
            conversion = dict(sorted(conversion_solides.items(), key=lambda item:[1]))
        else:
            return self.quantite

        for unite, valeur in conversion.items():
            if self.quantite >= valeur:
                return int(self.quantite / valeur)
            
        return None
    
    def get_unites(self):
        if self.type == 'liquide':
            return conversion_liquides.keys()
        elif self.type == 'solide':
            return conversion_solides.keys()
        else:
            return ['unite']
    
    def get_unite(self):
        if self.type == 'liquide':
            conversion = dict(sorted(conversion_liquides.items(), key=lambda item:[1]))
        elif self.type == 'solide':
            conversion = dict(sorted(conversion_solides.items(), key=lambda item:[1]))
        else:
            return 'unite'

        for unite, valeur in conversion.items():
            if self.quantite >= valeur:
                return unite
            
        return None
    
    def add_famille(self, famille):

        if famille is None or famille == '':
            return
        familles = [nom.strip() for nom in famille.replace('/', '+').split('+')]
        for nom_famille in familles:
            famille_obj, _ = Famille.objects.get_or_create(nom=nom_famille)
            self.familles.add(famille_obj)
        self.save()

    def add_fournisseur(self, fournisseur):
        self.fournisseur = Fournisseur.objects.get_or_create(nom=fournisseur)[0]
        self.save()