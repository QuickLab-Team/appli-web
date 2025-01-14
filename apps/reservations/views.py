from django.shortcuts import render, get_object_or_404
from .models import Reservation, MessageReservation
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# Vue pour la liste des réservations
@login_required
def reservations(request):
    reservations = Reservation.objects.all().order_by('-date')
    if request.user.role == 'preparateur':
        return render(request, 'reservations/preparateurs/reservations.html', {
            'titre': 'QuickLab',
            'reservations': reservations
        })
    else:
        return render(request, 'reservations/etudiants/reservations.html', {
            'titre': 'QuickLab',
            'reservations': reservations
        })

# Vue pour les détails d'une réservation
@login_required
def detail_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.user.role == 'preparateur':
        return render(request, 'reservations/preparateurs/reservation.html', {
            'reservation': reservation,
            'messages': reservation.messages.all().order_by('-date'),
            'titre': 'QuickLab'
        })
    else:
        return render(request, 'reservations/etudiants/detail_reservation.html', {
            'reservation': reservation,
            'messages': reservation.messages.all().order_by('-date')
        })

@login_required
def ajouter_message(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        message = request.POST.get('message')
        MessageReservation.objects.create(reservation=reservation, utilisateur=request.user, message=message)
        return JsonResponse({'erreur': False, 'message': 'Message ajouté'}, status=200)
    return HttpResponseNotAllowed(['POST'], 'Méthode non autorisée.')

@login_required
def annuler_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    reservation.etat = 'annule'
    reservation.save()

    for produit_reservation in reservation.produits.all():
        produit_reservation.produit.add_quantite(produit_reservation.quantite)
        produit_reservation.produit.save()

    return redirect('detail_reservation', reservation_id=reservation_id)