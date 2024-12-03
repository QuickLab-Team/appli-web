from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUtilisateurManager

# Create your models here.

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

    objects = CustomUtilisateurManager()

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions_set', blank=True)
    
    def __str__(self):
        return "{0} {1}".format(self.nom, self.prenom)
