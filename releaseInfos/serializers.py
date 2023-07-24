from .models import ReleaseInfo
from rest_framework import serializers


class ReleaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReleaseInfo
        fields = '__all__'