from django.urls import path
from . import views

app_name = 'produits'

urlpatterns = [
    path('', views.produits, name='produits'),
    path('<int:produit_id>/', views.produit, name='produit'),
    path('importer/', views.importer_produits, name='importer_produits'),
    path('ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('exporter/', views.exporter_produits, name='exporter_produits'),
    path('<int:produit_id>/modifier', views.modifier_produit, name='modifier_produit'),
    path('<int:produit_id>/supprimer', views.supprimer_produit, name='supprimer_produit'),
    path('add_service/', views.add_service, name='add_service'),
    path('fournisseurs/', views.fournisseurs, name='fournisseurs'),
    path('fournisseurs/ajouter/', views.ajouter_fournisseur, name='ajouter_fournisseur'),
    path('fournisseurs/<int:fournisseur_id>/modifier/', views.modifier_fournisseur, name='modifier_fournisseur'),
    path('fournisseurs/<int:fournisseur_id>/supprimer/', views.supprimer_fournisseur, name='supprimer_fournisseur'),
    path('fournisseurs/<int:fournisseur_id>/', views.fournisseur_detail, name='fournisseur_detail'),
    path('stockages/', views.stockages, name='stockages'),
    path('stockages/ajouter/', views.ajouter_stockage, name='ajouter_stockage'),
    path('stockages/<int:stockage_id>/modifier/', views.modifier_stockage, name='modifier_stockage'),
    path('stockages/<int:stockage_id>/supprimer/', views.supprimer_stockage, name='supprimer_stockage'),
    path('stockages/<int:stockage_id>/', views.stockage_detail, name='stockage_detail'),
]