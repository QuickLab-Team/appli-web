from django.shortcuts import render, redirect

# import pandas as pd
from .models import Produit, Service, Stockage
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Stockage
from django.contrib.auth.decorators import login_required
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
        return redirect("liste_produits")

    return render(request, "produits/preparateurs/importer.html", {
        "produits_preview": produits_preview
    })


def produit(request, produit_id):
    produit = Produit.objects.get(id=produit_id)
    panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
    return render(request, 'produits/etudiants/produit.html', {
        'titre': 'QuickLab',
<<<<<<< HEAD
        'produit': produit
    })
    
    
@login_required
def liste_stockages(request):
    """Affiche la liste des lieux de stockage avec filtres et actions."""
    query = request.GET.get('q', '')
    service_id = request.GET.get('service', '')

    stockages = Stockage.objects.all()
    services = Service.objects.all()

    if query:
        stockages = stockages.filter(nom__icontains=query)
    if service_id:
        stockages = stockages.filter(service_id=service_id)

    return render(request, 'produits/preparateurs/liste_stockage.html', {
        'stockages': stockages,
        'services': services,
        'query': query,
        'selected_service': service_id,
    })

@login_required
def ajouter_stockage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nom = data.get('nom')
        service_id = data.get('service')
        service = Service.objects.get(id=service_id) if service_id else None

        Stockage.objects.create(nom=nom, service=service)
        return JsonResponse({"success": True, "message": "Lieu de stockage ajouté avec succès."})

    services = Service.objects.all()
    return render(request, 'produits/ajouter_stockage.html', {'services': services})

@csrf_exempt
def supprimer_stockage(request, stockage_id):
    """Supprime un lieu de stockage."""
    if request.method == "POST":
        stockage = get_object_or_404(Stockage, id=stockage_id)
        stockage.delete()
        return JsonResponse({"success": True, "message": "Lieu de stockage supprimé avec succès."})
    
@login_required
def details_stockage(request, stockage_id):
    """Récupère les détails d'un stockage spécifique pour modification."""
    stockage = get_object_or_404(Stockage, id=stockage_id)
    services = Service.objects.all()

    data = {
        "success": True,
        "stockage": {
            "nom": stockage.nom,
            "service_id": stockage.service.id if stockage.service else None,
        },
        "services": [{"id": service.id, "nom": service.nom} for service in services],
    }

    return JsonResponse(data)

@login_required
def modifier_stockage(request, stockage_id):
    """Modifie un lieu de stockage existant."""
    if request.method == "POST":
        stockage = get_object_or_404(Stockage, id=stockage_id)
        data = json.loads(request.body)
        stockage.nom = data.get("nom", stockage.nom)
        service_id = data.get("service")
        stockage.service = Service.objects.get(id=service_id) if service_id else None
        stockage.save()
        return JsonResponse({"success": True, "message": "Lieu de stockage modifié avec succès."})
    
@login_required
def liste_stockages(request):
    """Affiche la liste des lieux de stockage avec filtres et actions."""
    query = request.GET.get('q', '')
    service_id = request.GET.get('service', '')

    stockages = Stockage.objects.all()
    services = Service.objects.all()

    if query:
        stockages = stockages.filter(nom__icontains=query)
    if service_id:
        stockages = stockages.filter(service_id=service_id)

    # Si la requête est AJAX, renvoyer uniquement la table mise à jour
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string(
            'produits/preparateurs/includes/stockages_table.html',
            {'stockages': stockages}
        )
        return JsonResponse({'success': True, 'html': html})

    return render(request, 'produits/preparateurs/liste_stockage.html', {
        'stockages': stockages,
        'services': services,
        'query': query,
        'selected_service': service_id,
=======
        'produit': produit,
        'in_panier': panier.produits.filter(produit=produit).exists()
>>>>>>> 651250e8b24e66a58314ad2d96b17687495bacae
    })