from django.db import models

class Utilisateur(models.Model):
    """
    Utilisateur
    """
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    
    def __str__(self):
        return "{0} {1}".format(self.nom, self.prenom)

class Produit(models.Model):
    """
    Produit
    """
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    quantite = models.IntegerField()
    description = models.TextField()
    unite = models.CharField(max_length=10)
    famille = models.ForeignKey('Famille', on_delete=models.CASCADE)
    stockage = models.ForeignKey('Stockage', on_delete=models.CASCADE, related_name='produits')
    
    def __str__(self):
        return "{0} {1}".format(self.id, self.nom)
    
class Stockage(models.Model):
    """
    Stockage
    """
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='stockages')
    
    def __str__(self):
        return "{0} {1}".format(self.id, self.nom)
    
class Service(models.Model):
    """
    Service
    """
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    
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

class Reservation(models.Model):
    """
    Reservation
    """
    id = models.AutoField(primary_key=True)
    utilisateur = models.ForeignKey('Utilisateur', on_delete=models.CASCADE)
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    date = models.DateField()
    quantite = models.IntegerField()
    unite = models.CharField(max_length=10)
    
    def __str__(self):
        return "{0} - {1} - {2} {3}".format(self.utilisateur, self.produit, self.quantite, self.unite)