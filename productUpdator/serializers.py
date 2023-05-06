#serializer for productupdater
from rest_framework import serializers
from .models import ProductUpdator, ProductUpdatorItems
from products.serializers import ProductSerializer
from products.models import kicks as product



        
        
        
class ProductUpdatorSerializer(serializers.ModelSerializer):
    class ProductForUpdatorSerializer(serializers.ModelSerializer):

        class Meta:
            model = product
            fields = ('name',)
    class ProductUpdatorItemSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductUpdatorItems
            fields = '__all__'

    productUpdatorItems = ProductUpdatorItemSerializer(many=True, read_only=True)
    product_info = ProductForUpdatorSerializer(source='product', required=False)
    class Meta:
        model = ProductUpdator
        fields = ('pk', 'user', 'created_at', 'product', 'final_approved', 'total_point', 'productUpdatorItems', 'product_info', )


    
        
        
        
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


