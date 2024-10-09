from django.urls import path
from . import views
from django.views.generic import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('produits/', views.Produits.as_view(), name='produits'),
    path('test/', views.Test.as_view(), name='tests'),
    path('reservations/', views.Reservations.as_view(), name='reservations'),
    # path('produits/<int:id>/', '', name='produit'),

    # path('famille/', '', name='familles'),
]
