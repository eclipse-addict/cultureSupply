from .models import kicks
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

class kicksSerializer(serializers.ModelSerializer):    
    # id = serializers.ReadOnlyField()
    reviews = ReviewListSerializer(many=True, read_only=True)
    count_reviews = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    class Meta:
        model = kicks
        fields = ('reviews', 'count_reviews','avg_rating', 'id', 'brand', 'colorway', 'description', 
                'gender', 'name', 'releaseDate', 'retailPrice', 'estimatedMarketValue', 
                'sku', 'imageUrl','local_imageUrl', 'like_users',)
    
    def get_count_reviews(self, obj):
        return obj.reviews.count()

    def get_avg_rating(self, ob):
        # reverse lookup on Reviews using item field
        return ob.reviews.all().aggregate(Avg('rating'))['rating__avg']

