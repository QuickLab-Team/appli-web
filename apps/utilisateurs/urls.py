from django.urls import path
from . import views
from .views import ConnexionView

urlpatterns = [
    path('accueil', views.accueil, name='accueil'),
    path('inscription/', views.inscription, name='inscription'),
    path('', ConnexionView.as_view(), name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
]
