from django.urls import path
from . import views

app_name = 'paniers'

urlpatterns = [
    path('', views.panier, name='panier'),
    path('ajouter', views.ajouter_produit_panier, name='ajouter_produit_panier'),
    path('supprimer', views.supprimer_produit_panier, name='supprimer_produit_panier'),
    path('modifier', views.modifier_produit_panier, name='modifier_produit_panier'),
    path('reserver', views.reserver_panier, name='reserver_panier'),
]