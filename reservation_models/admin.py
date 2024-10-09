from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Utilisateur)
admin.site.register(Produit)
admin.site.register(Stockage)
admin.site.register(Service)
admin.site.register(Famille)
admin.site.register(Reservation)
