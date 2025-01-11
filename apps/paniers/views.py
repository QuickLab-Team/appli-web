from django.shortcuts import render, get_object_or_404, redirect
from .models import Panier, PanierProduit
from produits.models import Produit
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from reservations.models import Reservation, ReservationProduit
from django.views.decorators.cache import never_cache

# Create your views here.
@never_cache
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

def modifier_quantite(request, produit_panier_id):
    if request.method == 'POST':
        quantite = int(request.POST.get('quantite'))
        unite = request.POST.get('unite')
        panier_produit = get_object_or_404(PanierProduit, id=produit_panier_id)
        panier_produit.quantite = 0
        panier_produit.add_quantite(quantite, unite)
        return JsonResponse({'erreur': False, 'message': 'Quantité modifiée'}, status=200)
    return HttpResponseNotAllowed(['POST'], 'Méthode non autorisée.')

def reserver_panier(request):
    panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
    if panier.produits.count() > 0:
        reservation = Reservation.objects.create(
            utilisateur=request.user,
        )
        for produit_panier in panier.produits.all():
            reservation_produit = ReservationProduit.objects.create(
                reservation=reservation,
                produit=produit_panier.produit,
                quantite=produit_panier.quantite,
            )
        
        panier.produits.all().delete()
        return redirect('detail_reservation', reservation.id)
    return redirect('panier')