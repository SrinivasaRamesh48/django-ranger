from rest_framework import serializers
from app.models.MeshCPEInstall import MeshCPEInstall # Import the MeshCPEInstall model

class MeshCPEInstallSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = MeshCPEInstall
        fields = '__all__' 
       