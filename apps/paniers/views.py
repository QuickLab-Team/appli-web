from django.shortcuts import render, get_object_or_404, redirect
from .models import Panier, PanierProduit
from produits.models import Produit

# Create your views here.

def panier(request):
    panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
    return render(request, 'paniers/etudiants/panier.html', {'panier': panier})

def ajout_panier(request, produit_id):
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite'))
        unite = request.POST.get('unite')
        produit = get_object_or_404(Produit, id=produit_id)
        panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
        panier_produit = PanierProduit.objects.create(panier=panier, produit=produit, quantite=0)
        panier_produit.add_quantite(quantite, unite)
    return redirect('panier')

def suppression_panier(request, produit_id):
    panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
    produit = get_object_or_404(Produit, id=produit_id)
    PanierProduit.objects.filter(panier=panier, produit=produit).delete()
    return redirect('panier')