from django.urls import path
from . import views
from .views import ConnexionView

app_name = 'utilisateurs'

urlpatterns = [
    path('accueil', views.accueil, name='accueil'),
    path('', views.accueil, name='accueil'),
    path('connexion/', ConnexionView.as_view(), name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('utilisateurs/', views.utilisateurs, name='utilisateurs'),
    path('ajouter_utilisateur/', views.ajouter_utilisateur, name='ajouter_utilisateur'),
    path('importer_utilisateurs/', views.importer_utilisateurs, name='importer_utilisateurs'),
    path('supprimer/', views.supprimer_utilisateurs, name='supprimer_utilisateurs'),
    path('modifier/<int:utilisateur_id>/', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('compte', views.compte, name='compte'),
]
