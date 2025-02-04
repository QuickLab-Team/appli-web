from django.urls import path
from . import views

app_name = 'produits'

urlpatterns = [
    path('', views.produits, name='produits'),
    path('<int:produit_id>/', views.produit, name='produit'),
    path('importer/', views.importer_produits, name='importer_produits'),
    path('ajouter/', views.ajouter_produit, name='ajouter_produit'),
    path('<int:produit_id>/modifier', views.modifier_produit, name='modifier_produit'),
    path('<int:produit_id>/supprimer', views.supprimer_produit, name='supprimer_produit'),
    path('add_service/', views.add_service, name='add_service'),
]