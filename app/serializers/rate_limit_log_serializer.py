from rest_framework import serializers
from app.models import RateLimitLog, Home
from app.serializers.home_serializer import HomeSerializer


class RateLimitLogSerializer(serializers.ModelSerializer):
    home = HomeSerializer(read_only=True)
    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    
    class Meta:
        model = RateLimitLog
        fields = [
            'rate_limit_log_id', 'success', 'rate', 'result', 
            'created_at', 'updated_at',
            'home', 'home_id'
        ]
