from django.shortcuts import render, get_object_or_404
from .models import Reservation, MessageReservation
from django.http import JsonResponse, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from produits.models import Famille, Service
from django.core.mail import send_mail

# Vue pour la liste des réservations
@login_required
def reservations(request):
    reservations = Reservation.objects.all().order_by('-date')
    if request.user.role in ['preparateur', 'administrateur']:
        return render(request, 'reservations/preparateurs/reservations.html', {
            'titre': 'QuickLab',
            'reservations': reservations
        })
    else:
        return render(request, 'reservations/etudiants/reservations.html', {
            'titre': 'QuickLab',
            'reservations': reservations,
            'familles': Famille.objects.all().distinct(),
            'services': Service.objects.all().distinct(),
        })

# Vue pour les détails d'une réservation
@login_required
def reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.user.role in ['preparateur', 'administrateur']:
        return render(request, 'reservations/preparateurs/reservation.html', {
            'reservation': reservation,
            'messages': reservation.messages.all().order_by('-date'),
            'titre': 'QuickLab',
        })
    else:
        return render(request, 'reservations/etudiants/reservation.html', {
            'reservation': reservation,
            'messages': reservation.messages.all().order_by('-date'),
            'familles': Famille.objects.all().distinct(),
            'services': Service.objects.all().distinct(),
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

    return redirect('reservations:reservation', reservation_id=reservation_id)

@login_required
def modifier_reservation_etat(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        etat = request.POST.get('etat')
        reservation.etat = etat
        reservation.save()

        # Envoyer un email uniquement si la commande est validée
        if etat == "valide":
            etudiant = reservation.utilisateur  # Supposons que Reservation a un champ `utilisateur`
            if etudiant and etudiant.email:
                message = f"""
                Bonjour {etudiant.prenom},

                Votre réservation #{reservation.id} a été validée par un préparateur.

                Vous pouvez venir récupérer votre commande dès que possible.

                Cordialement,
                L'équipe QuickLab
                """
                send_mail(
                    subject="Votre réservation a été validée",
                    message=message,
                    from_email='QuickLab <votre_email@gmail.com>',
                    recipient_list=[etudiant.email],
                    fail_silently=False,
                )

        return JsonResponse({'erreur': False, 'message': 'État modifié et email envoyé si validé'}, status=200)
    return HttpResponseNotAllowed(['POST'], 'Méthode non autorisée.')

