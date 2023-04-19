from .models import kicks, productImg
from rest_framework import serializers
from reviews.models import Review
from accounts.models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
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



class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewListSerializer(many=True, read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    like_count = serializers.IntegerField(read_only=True)
    rating_avg = serializers.IntegerField(read_only=True)

    class Meta:
        model = kicks
        fields = ('reviews', 'like_count', 'review_count', 'id',
                  'brand', 'colorway', 'description', 'category',
                  'gender', 'name', 'releaseDate', 'retailPrice',
                  'click', 'sku', 'local_imageUrl', 'like_users', 'rating_avg',)


class RecentReleaseSerializers(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ('id', 'name', 'local_imageUrl')