from django.urls import path
from . import views

urlpatterns = [
    path('', views.panier, name='panier'),
    path('ajout/<int:produit_id>/', views.ajout_panier, name='ajout_panier'),
    path('suppression/<int:produit_id>/', views.suppression_panier, name='suppression_panier'),
    path('modifier/<int:produit_panier_id>/', views.modifier_quantite_panier, name='modifier_quantite_panier'),
    path('reserver/', views.reserver_panier, name='reserver_panier'),
]