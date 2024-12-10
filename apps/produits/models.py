from django.db import models

# Create your models here.
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
    
class Produit(models.Model):
    """
    Produit
    """
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    quantite = models.FloatField()
    description = models.TextField()
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE)
    stockage = models.ForeignKey(Stockage, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[('liquide', 'Liquide'), ('solide', 'Solide'), ('unite', 'Unité')], default='unite')
    
    def __str__(self):
        return "{0} {1} {2}".format(self.id, self.nom, self.description)
    
    def add_quantite(self, quantite, unite):
        if self.type == 'liquide':
            switch = {
                'l': 1,
                'cl': 100,
                'ml': 1000
            }
        elif self.type == 'solide':
            switch = {
                'kg': 1,
                'g': 1000,
                'mg': 1000000
            }
        else:
            switch = {
                'unite': 1
            }
        quantite = quantite * switch[unite]
        self.quantite += quantite
        self.save()

    def get_unite(self):
        if self.type == 'liquide':
            if self.quantite >= 1:
                return 'l'
            elif self.quantite >= 0.1:
                return 'cl'
            else:
                return 'ml'
        elif self.type == 'solide':
            if self.quantite >= 1:
                return 'kg'
            elif self.quantite >= 0.001:
                return 'g'
            else:
                return 'mg'
        else:
            return 'unite'