from rest_framework import serializers
from products.models import kicks


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = kicks
        fields = ('sku', 'brand', 'colorway', 'description',
                  'category', 'gender', 'name', 'name_kr',
                  'releaseDate', 'retailPrice', 'local_imageUrl')