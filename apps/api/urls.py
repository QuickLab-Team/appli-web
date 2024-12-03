from django.urls import path
from . import views
from django.views.generic import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('test/', views.Test.as_view(), name='tests'),
    path('reservations/', views.Reservations.as_view(), name='reservations'),
    path('familles/', views.Familles.as_view(), name='familles'),
    path('produits/', views.Produits.as_view(), name='produits'),
    path('produit/<pk>/', views.Produit.as_view(), name='produit'),
]
