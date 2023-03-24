from .models import kicks, productImg
from rest_framework import serializers
from reviews.models import Review
from accounts.models import UserInfo
from django.db.models import Avg

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserInfo
        fields = '__all__'



class ReviewListSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Review
        fields = ('content', 'rating', 'created_at', 'like_users', 'dislike_users')
        
        
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_info'] = UserInfoSerializer(instance.user_info).data
        return response



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = productImg
        fields = '__all__'



class productListSerializer(serializers.ModelSerializer):   
    class Meta:
        model = kicks
        fields = ('id', 'brand', 'colorway', 'description', 'category', 
                'gender', 'name', 'releaseDate', 'retailPrice', 'estimatedMarketValue', 
                'sku', 'imageUrl','local_imageUrl', 'like_users',)
   
   


class productSerializer(serializers.ModelSerializer):    
    reviews       = ReviewListSerializer(many=True, read_only=True)
    productImg    = ProductImageSerializer(many=True, read_only=True)
    count_reviews = serializers.SerializerMethodField()
    avg_rating    = serializers.SerializerMethodField()
    class Meta:
        model = kicks
        fields = ('reviews', 'productImg', 'count_reviews','avg_rating', 'id', 'brand', 'colorway', 'description', 'category', 
                'gender', 'name', 'releaseDate', 'retailPrice', 'estimatedMarketValue', 
                'sku', 'local_imageUrl', 'like_users',)
        depth = 1
        
    def get_count_reviews(self, obj):
        return obj.reviews.count()

    def get_avg_rating(self, ob):
        # reverse lookup on Reviews using item field
        return ob.reviews.all().aggregate(Avg('rating'))['rating__avg']

