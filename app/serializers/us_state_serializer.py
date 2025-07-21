from rest_framework import serializers
from app.models import UsState


class UsStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsState
        fields = ['state_id', 'name', 'abbreviation']
