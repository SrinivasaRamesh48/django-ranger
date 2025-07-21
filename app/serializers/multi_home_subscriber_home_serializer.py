from rest_framework import serializers
from app.models import MultiHomeSubscriberHome, Home, Subscriber


class MultiHomeSubscriberHomeSerializer(serializers.ModelSerializer):
    home = serializers.SerializerMethodField()
    subscriber = serializers.SerializerMethodField()
    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    subscriber_id = serializers.PrimaryKeyRelatedField(queryset=Subscriber.objects.all(), source='subscriber', write_only=True)
    
    class Meta:
        model = MultiHomeSubscriberHome
        fields = [
            'multi_home_subscriber_home_id', 'created_at', 'updated_at',
            'home', 'subscriber', 'home_id', 'subscriber_id'
        ]        
        
    def get_home(self, obj):
        from app.serializers.home_serializer import HomeSerializer
        return HomeSerializer(obj.home).data if obj.home else None
        
    def get_subscriber(self, obj):
        from app.serializers.subscriber_serializer import SubscriberSerializer
        return SubscriberSerializer(obj.subscriber).data if obj.subscriber else None
