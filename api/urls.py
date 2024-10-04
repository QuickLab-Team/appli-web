from django.urls import path
from . import views
from django.views.generic import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import Home

urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'), 
]
