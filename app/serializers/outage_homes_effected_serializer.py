from rest_framework import serializers
from app.models import OutageHomesEffected, Home, Outage


class OutageHomesEffectedSerializer(serializers.ModelSerializer):
    home = serializers.SerializerMethodField()
    outage = serializers.SerializerMethodField()
    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    outage_id = serializers.PrimaryKeyRelatedField(queryset=Outage.objects.all(), source='outage', write_only=True)

    class Meta:
        model = OutageHomesEffected
        fields = '__all__'

    def get_home(self, obj):
        from app.serializers.home_serializer import HomeSerializer
        return HomeSerializer(obj.home).data if obj.home else None
        
    def get_outage(self, obj):
        from app.serializers.outage_serializer import OutageSerializer
        return OutageSerializer(obj.outage).data if obj.outage else None
