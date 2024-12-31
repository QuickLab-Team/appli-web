from django.shortcuts import render, get_object_or_404
from .models import Reservation

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