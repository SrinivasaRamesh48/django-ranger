from rest_framework import serializers
from app.models.RateLimitLog import RateLimitLog

class RateLimitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateLimitLog
        fields = '__all__'
