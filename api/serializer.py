from rest_framework import serializers
from reservation_models.models import *

# class ProduitFamilleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Produit
#         fields = ['id', 'nom']

# class ProduitStockageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Produit
#         fields = ['id', 'nom']

# class FamilleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Famille
#         fields = '__all__'

# class StockageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Stockage
#         fields = '__all__'

# class ProduitSerializer(serializers.ModelSerializer):
#     famille = ProduitFamilleSerializer()
#     stockage = ProduitStockageSerializer()
    
#     class Meta:
#         model = Produit
#         fields = '__all__'

class ReservationProduitSerializer(serializers.ModelSerializer):
    produit = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all())
    
    class Meta:
        model = ReservationProduit
        fields = ['produit', 'quantite']

class ReservationSerializer(serializers.ModelSerializer):
    produits = ReservationProduitSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ['utilisateur', 'produits']

    def create(self, validated_data):
        produits_data = validated_data.pop('produits')
        reservation = Reservation()
        reservation.utilisateur = Utilisateur.objects.get(id=1)
        reservation.save()
        for produit_data in produits_data:
            ReservationProduit.objects.create(reservation=reservation, produit=Produit.objects.get(id=1), quantite=200)
        return reservation
