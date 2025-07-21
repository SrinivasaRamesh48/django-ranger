from rest_framework import serializers
from app.models import Home


class HomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Home
        fields = ['home_id', 'address', 'city']
