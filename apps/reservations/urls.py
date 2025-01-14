from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservations, name='reservations'),
    path('<int:reservation_id>/', views.detail_reservation, name='detail_reservation'),
    path('ajouter_message/<int:reservation_id>/', views.ajouter_message, name='ajouter_message_reservation'),
    path('annuler/<int:reservation_id>/', views.annuler_reservation, name='annuler_reservation'),
]