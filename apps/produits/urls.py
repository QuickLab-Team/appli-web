from django.urls import path
from . import views

urlpatterns = [
    path('', views.produits, name='produits'),
]