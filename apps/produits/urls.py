from django.urls import path
from . import views
from paniers.views import ajout_panier

app_name = 'produits'


urlpatterns = [
    path('', views.produits, name='produits'),
    path('<int:produit_id>/', views.produit, name='produit'),
    path('ajout_panier/<int:produit_id>/', ajout_panier, name='ajout_panier'),
    path('importer/', views.importer_produits, name='importer_produits')
]