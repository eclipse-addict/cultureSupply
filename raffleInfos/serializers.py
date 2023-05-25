from rest_framework import serializers
from .models import Raffle, RaffleEntry
from products.serializers import ProductSerializer

class RaffleSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = Raffle
        fields = '__all__'
        read_only_fields = ('product',)



class RaffleEntrySerializer(serializers.ModelSerializer):
    raffle = RaffleSerializer()
    class Meta:
        model = RaffleEntry
        fields = '__all__'