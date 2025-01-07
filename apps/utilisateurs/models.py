from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUtilisateurManager

# Create your models here.

class Utilisateur(AbstractUser):
    ROLES = [
        ('etudiant', 'Etudiant'),
        ('preparateur', 'Preparateur'),
        ('administrateur', 'Administrateur'),
    ]
    
    ANNEES = [
        ('1A', '1ère Année'),
        ('2A', '2ème Année'),
        ('3A', '3ème Année'),
    ]
    
    id = models.AutoField(primary_key=True)
    role = models.CharField(max_length=100, choices=ROLES, default='etudiant')
    email = models.EmailField(unique=True)
    prenom = models.CharField(max_length=30)
    nom = models.CharField(max_length=30)
    annee = models.CharField(max_length=2, choices=ANNEES, blank=True, null=True)
    username = None 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['prenom', 'nom','role']

    objects = CustomUtilisateurManager()

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions_set', blank=True)
    
    def __str__(self):
        return "{0} {1}".format(self.prenom, self.nom)