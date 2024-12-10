from django.shortcuts import render
from .models import Produit

# Create your views here.

def produits(request):
    produits = Produit.objects.all()
    return render(request, 'produits/etudiants/produits.html', {
        'titre': 'QuickLab',
        'produits': produits
    })

def produit(request, produit_id):
    produit = Produit.objects.get(id=produit_id)
    return render(request, 'produits/etudiants/produit.html', {
        'titre': 'QuickLab',
        'produit': produit
    })