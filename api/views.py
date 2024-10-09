from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializer import *
    
# class Produits(APIView):

#     def get(self, request):
#         serializer = ProduitSerializer(Produit.objects.all(), many=True)
#         return Response(serializer.data)

class Test(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        quantite = 200
        produit = Produit.objects.get(id=1)

        reservation = Reservation()
        reservation.utilisateur = Utilisateur.objects.get(id=1)

        reservation_produit = ReservationProduit()
        reservation_produit.reservation = reservation
        reservation_produit.produit = produit
        reservation_produit.quantite = quantite

        reservation.save()
        reservation_produit.save()
        return Response("")
    
class Reservations(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        serializer = ReservationSerializer(Reservation.objects.all(), many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # utilisateur = Utilisateur.objects.create_user(
        #     id=1,
        #     email="test@gmail.com",
        #     nom="nom1",
        #     prenom="prenom1",
        #     password="motdepasse"
        # )
        # utilisateur.save()

        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

