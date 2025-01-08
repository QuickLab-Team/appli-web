from django.shortcuts import render, get_object_or_404
from .models import Reservation, ReservationProduit
from produits.models import Produit
from django.shortcuts import redirect

# Vue pour la liste des réservations
def reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/etudiants/reservations.html', {
        'titre': 'QuickLab',
        'reservations': reservations
    })

# Vue pour les détails d'une réservation
def detail_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    return render(request, 'reservations/etudiants/detail_reservation.html', {
        'reservation': reservation
    })

def ajout_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    panier = Reservation.objects.get_or_create(utilisateur=request.user, etat='panier')[0]
    ReservationProduit.objects.create(reservation=panier, produit=produit, quantite=1)
    return redirect('produit', produit_id=produit_id)