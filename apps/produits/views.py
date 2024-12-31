from django.shortcuts import render, redirect
# import pandas as pd
from .models import Produit
from django.contrib import messages
from .forms import FileImportForm

# Create your views here.

def produits(request):
    produits = Produit.objects.all()
    return render(request, 'produits/etudiants/produits.html', {
        'titre': 'QuickLab',
        'produits': produits
    })

# def importer(request):
#     if request.method == 'POST':
#         form = FileImportForm(request.POST, request.FILES)
#         if form.is_valid():
#             fichier = request.FILES['fichier']
#             if fichier.name.endswith('.csv'):
#                 df = pd.read_csv(fichier)
#             elif fichier.name.endswith('.xlsx'):
#                 df = pd.read_excel(fichier)
#             else:
#                 messages.error(request, 'Format de fichier non supporté.')
#                 return redirect('produits:importer_produits')

#             for _, row in df.iterrows():
#                 Produit.objects.create(
#                     nom=row['nom'],
#                     description=row['description'],
#                     prix=row['prix'],
#                     stock=row['stock']
#                 )
#             messages.success(request, 'Produits importés avec succès.')
#             return redirect('produits:produits')
#     else:
#         form = FileImportForm()

#     return render(request, 'produits/preparateurs/importer.html', {
#         'titre': 'QuickLab',
#         'form': form
#     })

def produit(request, produit_id):
    produit = Produit.objects.get(id=produit_id)
    return render(request, 'produits/etudiants/produit.html', {
        'titre': 'QuickLab',
        'produit': produit
    })