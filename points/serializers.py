from .models import Point, PointHistory
from rest_framework import serializers



class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = '__all__'
        read_only_fields = ( 'user',)


class PointHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PointHistory
        fields = '__all__'
        read_only_fields = ( 'user',)