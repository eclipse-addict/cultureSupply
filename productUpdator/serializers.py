#serializer for productupdater
from rest_framework import serializers
from .models import ProductUpdator, ProductUpdatorItems


class productUpdatorItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductUpdatorItems
        fields = '__all__'
        
        
        
class productUpdatorSerializer(serializers.ModelSerializer):
    
    updater_itmes = productUpdatorItemSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = ProductUpdator
        fields = ('user', 'product_id', 'updater_itmes',)
    
        
        
        
    # def create(self, validated_data):
    #     items_data = self['request'].data.get('updater_itmes')
    #     product_updater = ProductUpdator.objects.create(**validated_data)
    #     # images_data = self.context['request'].FILES
    #     # if images_data:
    #     #     for image_data in images_data.getlist('image'):
    #     #         ProductUpdatorItems.objects.create(product_updater=product_updater, **item_data)
    #     for item_data in items_data:
    #         ProductUpdatorItems.objects.create(product_updater=product_updater, **item_data)
    #     return product_updater


