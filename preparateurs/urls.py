from django.urls import path
from . import views
from .views import inscription, ConnexionView
from .views import accueil

urlpatterns = [
    path('', views.home, name='home'),
    path('accueil', views.accueil, name='accueil'),
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', ConnexionView.as_view(), name='connexion'),
    path('produits/', views.produits, name='produits'),
]
