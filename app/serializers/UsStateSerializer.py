# app/serializers.py

from rest_framework import serializers
from app.models.UsState import UsState 


class UsStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsState
        fields = '__all__' # This will include all fields from the model
        # Or explicitly list them:
        # fields = ['us_state_id', 'name', 'abbr', 'created_at', 'updated_at']