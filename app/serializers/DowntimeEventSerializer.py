from rest_framework import serializers
from app.models.DowntimeEvent import DowntimeEvent

# DowntimeEventSerializer.py
class DowntimeEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = DowntimeEvent
        fields = '__all__'
        