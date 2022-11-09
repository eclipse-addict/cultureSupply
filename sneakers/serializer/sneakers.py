from rest_framework import serializers
from ..models import Image, Sneaker
from django.contrib.auth import get_user_model

class likeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username',) # OOO님 외 299명이 좋아합니다. 구현을 위해 username return 

class SneakerListSerializer(serializers.ModelSerializer):
    
    like_users = likeUserSerializer(many=True)
    class Meta:
        model = Sneaker
        fields = ('pk','model_name','like_users',)
        
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', 'main_img',)

class SneakerDetailSerializer(serializers.ModelSerializer):
    # images = ImageSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField()
    
    def get_images(self, obj):
        images = obj.image_set.all()
        return ImageSerializer(instance=images, many=True).data
    class Meta:
        model  = Sneaker
        fields = ('model_name', 'release_date', 'describtion', 
                  'retail_price', 'images',)
        
    
    def create(self, validated_data):
        instance = Sneaker.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        
        for image_data in image_set.getlist('image'):
            Image.objects.create(sneaker=instance, image=image_data)
        return instance

