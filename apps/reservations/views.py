from django.shortcuts import render
from .models import *

# Create your views here.

def reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/etudiants/reservations.html', {
        'titre': 'QuickLab',
        'reservations': reservations
    })