from django.urls import path
from . import views
from paniers.views import ajouter_produit_panier

app_name = 'produits'

urlpatterns = [
    path('', views.produits, name='produits'),
    path('<int:produit_id>/', views.produit, name='produit'),
    path('ajouter_produit_panier/<int:produit_id>/', ajouter_produit_panier, name='ajouter_produit_panier'),
    path('importer/', views.importer_produits, name='importer_produits'),
    path('produit_detail/<int:produit_id>/', views.produit_detail, name='produit_detail'),
    path('ajouter_produit/', views.ajouter_produit, name='ajouter_produit'),
    path('modifier_produit/<int:produit_id>/', views.modifier_produit, name='modifier_produit'),
    path('supprimer_produit/<int:produit_id>/', views.supprimer_produit, name='supprimer_produit'),
]