from rest_framework import serializers
from app.models import UploadType


class UploadTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadType
        fields = ['upload_type_id', 'description']
