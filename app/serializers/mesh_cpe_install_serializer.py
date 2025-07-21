from rest_framework import serializers
from app.models import MeshCPEInstall, Home


class MeshCPEInstallSerializer(serializers.ModelSerializer):
    home = serializers.SerializerMethodField()
    home_id = serializers.PrimaryKeyRelatedField(queryset=Home.objects.all(), source='home', write_only=True)
    
    class Meta:
        model = MeshCPEInstall
        fields = [
            'mesh_cpe_install_id', 'address', 'cpe_id', 'cpe_serial_number',
            'created_at', 'updated_at',
            'home', 'home_id'
        ]
        
    def get_home(self, obj):
        from app.serializers.home_serializer import HomeSerializer
        return HomeSerializer(obj.home).data if obj.home else None
