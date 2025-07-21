from rest_framework import serializers
from app.models import OntManufacturer


class OntManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = OntManufacturer
        fields = ['ont_manufacturer_id']
