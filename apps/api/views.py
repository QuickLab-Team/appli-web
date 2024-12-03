from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import *

class Produit(APIView):

    def get(self, request):
        print(request)
        return Response("ok")
        # serializer = ProduitSerializer(produit)
        # return Response(serializer.data)

class Familles(APIView):
    
    def get(self, request):
        serializer = FamilleSerializer(Famille.objects.all(), many=True)
        return Response(serializer.data)
    
class Produits(APIView):

    def get(self, request):
        famille_id = request.GET.get('famille_id')
        produits = Produit.objects.all()
        
        if famille_id:
            produits = produits.filter(famille_id=famille_id)
        
        serializer = ProduitSerializer(produits, many=True)
        return Response(serializer.data)

class Test(APIView):

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        utilisateur = Utilisateur.objects.get(id=1)
        utilisateur.set_password("azertyuiop")
        utilisateur.save()
        return Response("")
    
class Reservations(APIView):

    def get(self, request):
        if request.user.is_anonymous:
            return Response([], status=401)
        reservations = Reservation.objects.filter(utilisateur=request.user)
        serializer = ReservationsSerializer(reservations, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ReservationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

