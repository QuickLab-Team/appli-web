from django.shortcuts import render, redirect
from .models import Produit, Famille, Stockage, Fournisseur
from django.contrib import messages
from .forms import FileImportForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import csv
from io import TextIOWrapper
import pandas as pd
import openpyxl

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


def importer_utilisateurs(request):
    produits_preview = []

    if request.method == "POST" and "fichier" in request.FILES:
        fichier = request.FILES["fichier"]
        df = pd.read_excel(fichier, skiprows=3)

        for _, row in df.iterrows():

            quantite = 0.0

            if row["Quantité"]:
                quantite_str = str(row["Quantité"])
                quantite = ''.join(filter(str.isdigit, quantite_str))
                unite = ''.join(filter(str.isalpha, quantite_str)).lower()
                quantite = float(quantite) if quantite else 0

            famille = row.get("Fonction")
            fournisseur = row.get("Fournisseur")

            famille = famille if pd.notna(famille) and famille != "-"else "Pas de famille"
            fournisseur = fournisseur if pd.notna(fournisseur) and fournisseur != "-" else "Pas de fournisseur"


            produits_preview.append({
                "nom": row["Produits"],
                "fournisseur": fournisseur,
                "quantite": quantite,
                "unite": unite,
                "famille": famille,
                "stockage": row["Lieu de stockage"],
            })

        request.session["produits_preview"] = produits_preview

    elif request.method == "POST" and "importer" in request.POST:
        produits_preview = request.session.get("produits_preview", [])

        for produit in produits_preview:
                
                
                p = Produit.objects.create(
                    nom=produit["nom"],
                    quantite=0,
                    
                    stockage=Stockage.objects.get_or_create(nom=produit["stockage"], service=Stockage.objects.first().service)[0],
                )

                if produit["famille"] != "Pas de famille":
                    p.add_famille(produit["famille"])
            

                if produit["fournisseur"] != "Pas de fournisseur":
                    p.add_fournisseur(produit["fournisseur"])

                if produit["quantite"]  and produit["unite"]:
                    p.add_type(produit["unite"])
                    p.add_quantite(produit["quantite"], produit["unite"])

        del request.session["produits_preview"]
        return redirect("produits")

    return render(request, "produits/preparateurs/importer.html", {
        "produits_preview": produits_preview
    })


def produit(request, produit_id):
    produit = Produit.objects.get(id=produit_id)
    panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
    return render(request, 'produits/etudiants/produit.html', {
        'titre': 'QuickLab',
        'produit': produit,
        'in_panier': panier.produits.filter(produit=produit).exists()
    })