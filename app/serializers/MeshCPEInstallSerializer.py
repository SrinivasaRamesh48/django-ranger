# app/serializers.py

from rest_framework import serializers
from app.models.MeshCPEInstall import MeshCPEInstall # Import the MeshCPEInstall model
# from .serializers import HomeSerializer # If you want nested Home representation

# ... (your other serializers) ...

class MeshCPEInstallSerializer(serializers.ModelSerializer):
    # home = HomeSerializer(read_only=True) # If you want nested Home representation

    class Meta:
        model = MeshCPEInstall
        fields = '__all__' # This will include all fields from the model
        # Or specify explicit fields if you don't want to expose all:
        # fields = [
        #     'mesh_cpe_install_id', 'home', 'address', 'cpe_id', 'cpe_serial_number',
        #     'created_at', 'updated_at', 'deleted_at'
        # ]