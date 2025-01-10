from django.shortcuts import render, redirect
from .models import Produit, Famille, Stockage, Fournisseur
from django.contrib import messages
from .forms import FileImportForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import csv
from io import TextIOWrapper
import pandas as pd

from paniers.models import Panier

# Create your views here.

def produits(request):
    produits = Produit.objects.all()
    familles = Famille.objects.all()
    stockages = Stockage.objects.all()

    if request.user.role == 'etudiant':
        return render(request, 'produits/etudiants/produits.html', {
        'titre': 'QuickLab',
        'produits': produits
    })

    elif request.user.role == 'preparateur' or request.user.role == 'administrateur':
        nom_query = request.GET.get('nom')
        famille_query = request.GET.get('famille')
        stockage_query = request.GET.get('stockage')
        if nom_query:
            produits = produits.filter(nom__icontains=nom_query)
        if famille_query:
            produits = produits.filter(famille__nom=famille_query)
        if stockage_query:
            produits = produits.filter(stockage__nom=stockage_query)
        return render(request, 'produits/preparateurs/produits.html', {
            'titre': 'QuickLab',
            'famille': familles,
            'stockage': stockages,
            'produits': produits,
            'nom_query': nom_query,
            'famille_query': famille_query,
            'stockage_query': stockage_query

        })

    
@login_required
def importer_produits(request):
    if request.method == 'POST' and request.FILES['fichier']:
        fichier = request.FILES['fichier']
        fs = FileSystemStorage()
        filename = fs.save(fichier.name, fichier)
        uploaded_file_url = fs.url(filename)

        with open(fs.path(filename), mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the first line
            for row in reader:
                Produit.objects.create(
                    nom=row[0],
                    famille=Famille.objects.get_or_create(nom=row[1])[0],
                    quantite=10.0,
                    fournisseur=Fournisseur.objects.get_or_create(nom=row[1])[0],
                    stockage=Stockage.objects.get_or_create(nom=row[2], service=Stockage.objects.first().service)[0],
                )
        messages.success(request, 'Produits importés avec succès.')
        return render(request, 'produits/preparateurs/importer.html', {
            'uploaded_file_url': uploaded_file_url
        })
    
    return render(request, 'produits/preparateurs/importer.html')

def produit(request, produit_id):
    produit = Produit.objects.get(id=produit_id)
    panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
    return render(request, 'produits/etudiants/produit.html', {
        'titre': 'QuickLab',
        'produit': produit,
        'in_panier': panier.produits.filter(produit=produit).exists()
    })