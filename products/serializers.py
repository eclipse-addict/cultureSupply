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



class ProductListSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = kicks
        fields = ('id', 'brand', 'colorway', 'description', 'category', 'click',
                  'gender', 'name', 'releaseDate', 'retailPrice', 'estimatedMarketValue',
                  'sku', 'imageUrl', 'local_imageUrl', 'like_users', 'reviews',
                  'review_count', 'like_count',)

    def get_avg_rating(self, ob):
        # reverse lookup on Reviews using item field
        return ob.reviews.all().aggregate(Avg('rating'))['rating__avg']

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = kicks
        fields = ('reviews', 'like_count', 'review_count', 'id', 'brand', 'colorway', 'description', 'category',
                  'gender', 'name', 'releaseDate', 'retailPrice', 'click', 'sku', 'local_imageUrl', 'like_users',)
        depth = 1


    # def get_count_reviews(self, obj):
    #     return obj.reviews.count()
    #
    #
    # def get_avg_rating(self, ob):
    #     # reverse lookup on Reviews using item field
    #     return ob.reviews.all().aggregate(Avg('rating'))['rating__avg']

