from rest_framework import serializers
from produits.models import *
from reservations.models import *

class StockageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stockage
        fields = '__all__'

class FamilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Famille
        fields = '__all__'

class ProduitSerializer(serializers.ModelSerializer):
    famille = FamilleSerializer()
    stockage = StockageSerializer()

    class Meta:
        model = Produit
        fields = '__all__'

class ReservationProduitSerializer(serializers.ModelSerializer):
    produit = ProduitSerializer()
    
    class Meta:
        model = Produit
        fields = ['quantite', 'produit']

class ReservationsSerializer(serializers.ModelSerializer):
    produits = ReservationProduitSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ['id', 'date', 'produits']

class ReservationProduitSerializer(serializers.ModelSerializer):
    produit = serializers.PrimaryKeyRelatedField(queryset=Produit.objects.all())
    
    class Meta:
        model = ReservationProduit
        fields = ['produit', 'quantite']

class ReservationSerializer(serializers.ModelSerializer):
    produits = ReservationProduitSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ['produits']

    def create(self, validated_data):
        produits_data = validated_data.pop('produits')
        utilisateur = utilisateur = self.context['request'].user
        reservation = Reservation.objects.create(utilisateur=utilisateur)
        for produit_data in produits_data:
            ReservationProduit.objects.create(reservation=reservation, produit=produit_data['produit'], quantite=produit_data['quantite'])
        return reservation
    
    def is_valid(self, *, raise_exception=False):
        for produit_data in self.initial_data.get('produits', []):
            produit = Produit.objects.filter(id=produit_data['produit']).first()
            if produit is None:
                message = {
                    'message': 'Produit '+str(produit_data['produit'])+' introuvable',
                }
                raise serializers.ValidationError(message)
        return super().is_valid(raise_exception=raise_exception)
