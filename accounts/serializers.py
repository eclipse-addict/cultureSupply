from .models import User, UserInfo
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user
    
class UserInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserInfo
        fields = '__all__'
        read_only_fields = ( 'user',)