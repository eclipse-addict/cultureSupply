from .models import kicks
from rest_framework import serializers
from reviews.models import Review
from accounts.models import UserInfo
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

class kicksSerializer(serializers.ModelSerializer):    
    reviews = ReviewListSerializer(many=True, read_only=True)
    class Meta:
        model = kicks
        fields = ('reviews', 'id', 'brand', 'colorway', 'description', 
                'gender', 'name', 'releaseDate', 'retailPrice', 'estimatedMarketValue', 
                'sku', 'imageUrl','local_imageUrl', 'like_users',)

