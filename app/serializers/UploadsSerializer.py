# app/serializers.py

from rest_framework import serializers
from app.models.Uploads import Uploads 

from app.models.UploadTypes import UploadType 

class UploadsSerializer(serializers.ModelSerializer):
    # For FileField, DRF usually provides the URL for read operations.
    # For write operations, clients will send the file data.

    # Optional: For nested representations
    # project = ProjectSerializer(read_only=True)
    # circuit = CircuitSerializer(read_only=True)
    # home = HomeSerializer(read_only=True)
    # subscriber = SubscriberSerializer(read_only=True)
    # upload_type = UploadTypeSerializer(read_only=True)

    class Meta:
        model = Uploads
        fields = '__all__' # This will include all fields from the model
        # You might want to make 'path' read_only if you only want to display the URL,
        # and handle the actual file upload via a custom view or serializer method.
        # But for direct ModelViewSet, it usually works if client sends file via multipart/form-data.
        # extra_kwargs = {
        #    'path': {'read_only': True} # If you only want to display URL, not take file via serializer
        # }
        # Or specify explicit fields:
        # fields = [
        #     'upload_id', 'project', 'circuit', 'home', 'subscriber', 'upload_type',
        #     'name', 'path', 'created_at', 'updated_at'
        # ]
        
class UploadTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadType
        fields = '__all__' # This will include all fields from the model        