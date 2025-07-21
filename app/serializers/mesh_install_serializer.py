from rest_framework import serializers
from app.models import MeshCPEInstall


class MeshInstallSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeshCPEInstall
        fields = ['mesh_cpe_install_id', 'address', 'cpe_id']
