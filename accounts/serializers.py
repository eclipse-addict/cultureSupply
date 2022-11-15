from .models import CustomUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            first_name= validated_data['first_name'],
            last_name= validated_data['last_name'],
        )
        return user
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 
                  'password',]