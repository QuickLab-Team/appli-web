from django.urls import path
from . import views
from .views import ConnexionView
from django.contrib.auth import views as auth_views

app_name = 'utilisateurs'

urlpatterns = [
    path('accueil', views.accueil, name='accueil'),
    path('home', views.test, name='home'),
    path('inscription/', views.inscription, name='inscription'),
    path('', ConnexionView.as_view(), name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('liste_utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('ajouter_utilisateur/', views.ajouter_utilisateur, name='ajouter_utilisateur'),
    path('importer_utilisateurs/', views.importer_utilisateurs, name='importer_utilisateurs'),
    path('supprimer/', views.supprimer_utilisateurs, name='supprimer_utilisateurs'),
    path('modifier/<int:utilisateur_id>/', views.modifier_utilisateur, name='modifier_utilisateur'),
    path('mon_compte/', views.mon_compte, name='mon_compte'),
    path('changer_mot_de_passe/', views.changer_mot_de_passe, name='changer_mot_de_passe'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('statistiques/', views.statistiques, name='statistiques'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]