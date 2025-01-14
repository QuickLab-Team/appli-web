from django.urls import path
from . import views
from paniers.views import ajout_panier

app_name = 'produits'


app_name = "produits"

urlpatterns = [
    path('', views.produits, name='liste_produits'),
    path('<int:produit_id>/', views.produit, name='produit'),
    path('ajout_panier/<int:produit_id>/', ajout_panier, name='ajout_panier'),
<<<<<<< HEAD
    
    path('stockages/', views.liste_stockages, name='liste_stockages'),
    path('stockages/ajouter/', views.ajouter_stockage, name='ajouter_stockage'),
    path('stockages/supprimer/<int:stockage_id>/', views.supprimer_stockage, name='supprimer_stockage'),
    path('stockages/<int:stockage_id>/', views.details_stockage, name='details_stockage'),
    path('stockages/modifier/<int:stockage_id>/', views.modifier_stockage, name='modifier_stockage'),
=======
    path('importer/', views.importer_utilisateurs, name='importer_produits')
>>>>>>> 651250e8b24e66a58314ad2d96b17687495bacae
]