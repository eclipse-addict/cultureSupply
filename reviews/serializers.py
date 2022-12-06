from .models import Review
from rest_framework import serializers

class kicksReviewSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ( 'user', 'product',)
