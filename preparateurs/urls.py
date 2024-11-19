from django.urls import path
from . import views
from .views import inscription, ConnexionView
from .views import accueil

urlpatterns = [
    path('', accueil, name='accueil'),
    path('inscription/', inscription, name='inscription'),
    path('connexion/', ConnexionView.as_view(), name='connexion'),
]
