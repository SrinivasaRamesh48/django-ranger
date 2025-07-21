from rest_framework import serializers
from app.models import ProjectNetworkType


class ProjectNetworkTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectNetworkType
        fields = ["__all__"]
