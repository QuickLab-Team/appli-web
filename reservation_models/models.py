from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager

class Utilisateur(AbstractUser):
    """
    Utilisateur
    """
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    role = models.CharField(max_length=100)
    username = None 

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "nom",
        "prenom",
    ]

    objects = CustomUserManager()

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions_set', blank=True)
    
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
    famille = models.ForeignKey('Famille', on_delete=models.CASCADE)
    stockage = models.ForeignKey('Stockage', on_delete=models.CASCADE)
    
    def __str__(self):
        return "{0} {1}".format(self.id, self.nom, self.description)
    
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
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return "{0}".format(self.utilisateur)

class ReservationProduit(models.Model):
    """
    ReservationProduit
    """
    id = models.AutoField(primary_key=True)
    reservation = models.ForeignKey('Reservation', related_name='produits', on_delete=models.CASCADE)
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    quantite = models.IntegerField()
    
    def __str__(self):
        return "{0} - {1} - {2}".format(self.reservation, self.produit, self.quantite)