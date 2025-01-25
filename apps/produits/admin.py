from django.contrib import admin
from .models import Service, Stockage, Famille, Fournisseur, Produit

admin.site.register(Service)
admin.site.register(Stockage)
admin.site.register(Famille)
admin.site.register(Fournisseur)
admin.site.register(Produit)