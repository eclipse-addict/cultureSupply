from .models import Review
from rest_framework import serializers
from accounts.models import UserInfo




class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserInfo
        fields = '__all__'
        
        
        
class kicksReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ( 'user', 'product', 'user_info')
        
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user_info'] = UserInfoSerializer(instance.user_info).data
        return response