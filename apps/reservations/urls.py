from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservations, name='reservations'),
    path('<int:reservation_id>/', views.reservation, name='reservation'),
    path('ajouter_message/<int:reservation_id>/', views.ajouter_message, name='ajouter_message_reservation'),
    path('annuler/<int:reservation_id>/', views.annuler_reservation, name='annuler_reservation'),
]