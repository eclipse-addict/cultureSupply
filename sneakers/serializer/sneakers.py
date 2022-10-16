from rest_framework import serializers
from ..models import Sneaker

class SneakerListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sneaker
        fields = ('model_name', 'retail_price',)


class SneakerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Sneaker
        fields = '__all__'

