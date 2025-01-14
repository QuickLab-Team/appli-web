from django.urls import path
from . import views
from .views import ConnexionView

app_name = 'utilisateurs'

urlpatterns = [
    path('accueil', views.accueil, name='accueil'),
    path('home', views.home, name='home'),
    path('inscription/', views.inscription, name='inscription'),
    path('', ConnexionView.as_view(), name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('liste_utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('ajouter_utilisateur/', views.ajouter_utilisateur, name='ajouter_utilisateur'),
    path('importer_utilisateurs/', views.importer_utilisateurs, name='importer_utilisateurs'),
    path('compte', views.compte, name='compte'),
]
