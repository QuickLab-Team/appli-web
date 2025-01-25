from django.shortcuts import render, get_object_or_404, redirect
from .models import Panier, PanierProduit
from produits.models import Famille, Service
from produits.models import Produit
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from reservations.models import Reservation, ReservationProduit
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required

# Create your views here.
@never_cache
@login_required
def panier(request):
    if request.user.role == 'etudiant':
        panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
        return render(request, 'paniers/etudiants/panier.html', {
            'panier': panier,
            'familles': Famille.objects.all().distinct(),
            'services': Service.objects.all().distinct(),
        })
    else:
        return HttpResponse('Page non trouvée', status=404)

@login_required
def ajouter_produit_panier(request):
    if request.user.role == 'etudiant':
        if request.method == 'POST':
            quantite = request.POST.get('quantite')
            if quantite is None:
                return HttpResponse('Veuillez renseigner une quantité.', status=400)

            unite = request.POST.get('unite')
            if unite is None:
                return HttpResponse('Veuillez renseigner une unité.', status=400)
            
            produit = get_object_or_404(Produit, id=request.POST.get('produit_id'))

            panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
            panier_produit = PanierProduit.objects.create(panier=panier, produit=produit, quantite=0)
            panier_produit.add_quantite(float(quantite), unite)

            return redirect('paniers:panier')

        return HttpResponseNotAllowed(['POST'], 'Méthode non autorisée.')
    else:
        return HttpResponse('Page non trouvée', status=404)

@login_required
def supprimer_produit_panier(request):
    if request.user.role == 'etudiant':
        if request.method == 'POST':

            produit = get_object_or_404(Produit, id=request.POST.get('produit_id'))
            panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
            PanierProduit.objects.filter(panier=panier, produit=produit).delete()

            return redirect('paniers:panier')
        
        return HttpResponseNotAllowed(['POST'], 'Méthode non autorisée.')
    
    else:
        return HttpResponse('Page non trouvée', status=404)

@login_required
def modifier_produit_panier(request):
    if request.user.role == 'etudiant':
        if request.method == 'POST':

            quantite = request.POST.get('quantite')
            if quantite is None:
                return HttpResponse('Veuillez renseigner une quantité.', status=400)

            unite = request.POST.get('unite')
            if unite is None:
                return HttpResponse('Veuillez renseigner une unité.', status=400)

            produit = get_object_or_404(Produit, id=request.POST.get('produit_id'))
            
            panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
            panier_produit = PanierProduit.objects.filter(panier=panier, produit=produit).first()
            panier_produit.quantite = 0
            panier_produit.add_quantite(int(quantite), unite)

            return redirect('paniers:panier')

        return HttpResponseNotAllowed(['POST'], 'Méthode non autorisée.')
    
    else:
        return HttpResponse('Page non trouvée', status=404)

@login_required
def reserver_panier(request):
    if request.user.role == 'etudiant':
        if request.method == 'POST':

            panier = Panier.objects.get_or_create(utilisateur=request.user)[0]
            if panier.produits.count() > 0:

                titre = 'Réservation'

                if request.POST.get('titre'):
                    titre = request.POST.get('titre')

                etat = 'attente'
                for produit_panier in panier.produits.all():
                    if produit_panier.produit.quantite < produit_panier.quantite:
                        etat = 'pre_reservation_attente'

                reservation = Reservation.objects.create(
                    utilisateur=request.user,
                    titre=titre,
                    etat=etat
                )
                for produit_panier in panier.produits.all():
                    reservation_produit = ReservationProduit.objects.create(
                        reservation=reservation,
                        produit=produit_panier.produit,
                        quantite=produit_panier.quantite,
                    )

                    produit_panier.produit.add_quantite(-produit_panier.quantite)
                
                panier.produits.all().delete()
                
                return redirect('reservations:reservation', reservation.id)
            
            else:
                return HttpResponse('Le panier est vide.', status=400)
        
        return HttpResponseNotAllowed(['POST'], 'Méthode non autorisée')
    
    else:
        return HttpResponse('Page non trouvée', status=404)