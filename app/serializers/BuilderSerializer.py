from rest_framework import serializers
from app.models.Builder import Builder


class BuilderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Builder
        fields = '__all__'