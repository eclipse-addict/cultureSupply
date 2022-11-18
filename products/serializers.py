from .models import kicks
from rest_framework import serializers

class kicksSerializer(serializers.ModelSerializer):
    
     class Meta:
         model = kicks
         fields = '__all__'
         
