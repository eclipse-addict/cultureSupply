from rest_framework import serializers
from ..models import Sneaker
from django.contrib.auth import get_user_model

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username',) # OOO님 외 299명이 좋아합니다. 구현을 위해 username return 

class SneakerListSerializer(serializers.ModelSerializer):
    
    like_users = userSerializer(many=True)
    class Meta:
        model = Sneaker
        fields = ('pk','model_name','main_img','like_users',)
        

class SneakerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model  = Sneaker
        fields = '__all__'

