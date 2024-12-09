from django.shortcuts import render
from .models import Produit

# Create your views here.

def produits(request):
    produits = Produit.objects.all()
    return render(request, 'produits/etudiants/produits.html', {
        'titre': 'QuickLab',
        'produits': produits
    })