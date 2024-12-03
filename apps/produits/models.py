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
    quantite = models.IntegerField()
    description = models.TextField()
    famille = models.ForeignKey(Famille, on_delete=models.CASCADE)
    stockage = models.ForeignKey(Stockage, on_delete=models.CASCADE)
    
    def __str__(self):
        return "{0} {1} {2}".format(self.id, self.nom, self.description)