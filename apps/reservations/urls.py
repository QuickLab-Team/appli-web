from django.urls import path
from . import views

urlpatterns = [
    path('', views.reservations, name='reservations'),
    path('<int:reservation_id>/', views.detail_reservation, name='detail_reservation'),
]